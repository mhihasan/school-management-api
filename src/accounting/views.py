import logging
from collections import OrderedDict
from datetime import datetime, timedelta
from decimal import Decimal
from itertools import groupby

from django.db import transaction
from django.db.models import Sum, F, Q, Case, When
from django.db.models.functions import Coalesce
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from src.accounting.base import (
    DueEntryView,
    BasePaymentViewSet,
    BaseInvoiceViewSet,
    BaseJournalViewSet,
)
from src.accounting.models import (
    AccountGroup,
    Account,
    Transaction,
    Journal,
    Invoice,
    Payment,
)
from src.accounting.serializers import (
    VoucherSerializer,
    InvoiceReportSerializer,
    PaymentReportSerializer,
    JournalEntryReportSerializer,
)
from src.api.v1.paginations import LimitOffsetUnlimitedDefaultPagination
from src.api.v1.viewsets import BaseViewSet
from . import serializers

console = logging.getLogger("console")
error_logger = logging.getLogger("accounting.error")
warning_logger = logging.getLogger("accounting.warning")


class AccountGroupViewSet(viewsets.ModelViewSet):
    queryset = AccountGroup.objects.all()
    serializer_class = serializers.AccountGroupSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("code", "name")

    pagination_class = LimitOffsetUnlimitedDefaultPagination


class COAViewSet(BaseViewSet):
    queryset = (
        Account.objects.all()
        .prefetch_related("transactions")
        .select_related("organization", "group")
    )
    serializer_class = serializers.COASerializer
    search_fields = ("code", "name")

    def get_queryset(self):
        status = {"active": 1, "inactive": -1}.get(self.request.GET.get("status"), 0)
        qs = super().get_queryset()
        if status == 1:
            qs = qs.filter(children__isnull=True, is_active=True)
        elif status == -1:
            qs = qs.filter(is_active=False)

        group_text = self.request.GET.get("group", None)
        if group_text:
            code = {"cash": [1], "revenue": [15, 16], "purchase": [18]}.get(group_text)
            if code:
                qs = qs.filter(group__code__in=code)

        group_id = self.request.GET.get("group_id", None)
        if group_id:
            qs = qs.filter(group_id=group_id)

        return qs

    def perform_create(self, serializer):
        """
        No group user, only organization admin staff can create chart of account. This account will be propagated to
        branches of this organization.

        """
        with transaction.atomic():
            # only organization admin staff can create chart of account
            if self.request.user.is_admin_staff:
                instance = super().perform_create(serializer)
                self.validate_account(instance)
            else:
                raise ValidationError(
                    "Only organization Admin Staff can create chart of account"
                )

    def perform_update(self, serializer):
        with transaction.atomic():
            instance = super().perform_update(serializer)
            self.validate_account(instance)
            if not instance.editable:
                raise ValidationError("You cannot edit this account")
            if instance.is_invalid():
                raise ValidationError(
                    "This account has already transactions. You cannot 'inactive'"
                )
            if instance.is_active:
                for d in instance.get_descendants():
                    if d.is_active:
                        raise ValidationError(
                            "This account has `active` descendant account"
                        )

    def perform_destroy(self, instance):
        if not instance.editable:
            raise ValidationError("You cannot delete this account")
        if instance.transactions.exists():
            raise ValidationError(
                "You cannot delete chart of accounts which has transactions"
            )
        return super().perform_destroy(instance)

    def validate_account(self, instance):
        def invalidated_debit(account):
            validated_depreciation_account = (
                account.group_id == 6 and account.balance_type == -1
            )
            if validated_depreciation_account:
                return False
            return (
                account.group.category in [0, 1, 8, 9, 10, 11]
                and account.balance_type == -1
            )

        def invalidated_credit(account):
            return (
                account.group.category in [2, 3, 4, 5, 6, 7]
                and account.balance_type == 1
            )

        def invalidated_depreciation_account(account):
            return account.group_id == 6 and account.balance_type == 1

        if invalidated_depreciation_account(instance):
            raise ValidationError(
                "`Accumulated Depreciation` must be Credit type Asset"
            )
        elif invalidated_debit(instance):
            raise ValidationError("This Account should be Debit type balance")
        elif invalidated_credit(instance):
            raise ValidationError("This Account should be Credit type balance")


class TransactionViewSet(BaseViewSet):
    queryset = Transaction.objects.all().select_related("account")
    serializer_class = serializers.TransactionSerializer
    http_method_names = ["delete"]


class JournalViewSet(BaseJournalViewSet):
    pass


class InvoiceViewSet(BaseInvoiceViewSet):
    serializer_class = serializers.InvoiceSerializer
    document_type = 0


class BillingEntryViewSet(BaseInvoiceViewSet):
    serializer_class = serializers.BillingEntrySerializer
    document_type = 1


class CreditNoteEntryViewSet(BaseInvoiceViewSet):
    serializer_class = serializers.CreditNoteEntrySerializer
    document_type = 2


class DebitNoteEntryViewSet(BaseInvoiceViewSet):
    serializer_class = serializers.DebitNoteEntrySerializer
    document_type = 3


class CollectionEntryViewSet(BasePaymentViewSet):
    """
    View set for collection for invoice to student

    """

    serializer_class = serializers.CollectionEntrySerializer
    type = 0


class PaymentViewSet(BasePaymentViewSet):
    """
    View set for payment for billing to teacher

    """

    serializer_class = serializers.PaymentSerializer
    type = 1


class DueInvoiceView(DueEntryView):
    serializer_class = serializers.DueInvoiceSerializer
    document_type = [0, 2]


class DueBillingView(DueEntryView):
    serializer_class = serializers.DueBillingEntrySerializer
    document_type = [1, 3]


class AgedView(viewsets.ViewSet):
    def date_range_dict(self, start, end):
        today = datetime.now()
        if start and end:
            r = {"due_date__range": (today - timedelta(start), today - timedelta(end))}
        elif end is None:
            r = {"due_date__lt": today - timedelta(360)}
        else:
            r = {"due_date__gte": today}

        return r

    def list(self, request):
        def bill(start, end=None):
            r = self.date_range_dict(start, end)
            return Coalesce(Sum("transactions__net_amount", filter=Q(**r)), 0)

        def pay(start, end=None):
            r = self.date_range_dict(start, end)
            return Coalesce(Sum("payments__amount", filter=Q(**r)), 0)

        invoices = Invoice.objects.filter(
            organization_id=self.request.user.organization_id, **self.filters
        )
        self.values.extend(
            [
                "document_type",
                "number",
                "current",
                "_1_30",
                "_31_60",
                "_61_90",
                "_91_180",
                "_181_360",
                "_361_infinity",
            ]
        )
        bills = invoices.annotate(
            current=bill(None, 0),
            _1_30=bill(30, 1),
            _31_60=bill(60, 31),
            _61_90=bill(90, 61),
            _91_180=bill(120, 91),
            _181_360=bill(360, 181),
            _361_infinity=bill(361),
        ).values(*self.values)

        payments = invoices.annotate(
            current=pay(None, 0),
            _1_30=pay(30, 1),
            _31_60=pay(60, 31),
            _61_90=pay(90, 61),
            _91_180=pay(120, 91),
            _181_360=pay(360, 181),
            _361_infinity=pay(361),
        ).values(*self.values)

        filtered = []
        fields = ["current", "_1_30", "_61_90", "_91_180", "_181_360", "_361_infinity"]

        for i, j in zip(bills, payments):
            total_bill = sum(i[f] for f in fields)

            if total_bill <= 0:
                continue
            total = 0
            for f in fields:
                i[f] -= j[f]
                total += i[f]
            i["total"] = total
            if total <= 0:
                continue
            i["number"] = (
                {0: "INV-{}", 1: "BILL-{}"}.get(i["document_type"]).format(i["number"])
            )

            filtered.append(i)

        return Response(filtered)


class AgedReceivableView(AgedView):
    """
    DOC_TYPE = (
        (0, 'Invoice'),
        (1, 'Billing'),
    )
    """

    values = ["student__code", "student__name"]
    filters = {
        "student__isnull": False,
        "document_type": 0,
        "due_date__isnull": False,
        "is_posted": True,
    }


class AgedPayableView(AgedView):
    """
    DOC_TYPE = (
        (0, 'Invoice'),
        (1, 'Billing'),
    )
    """

    values = ["teacher__code", "teacher__name"]
    filters = {
        "teacher__isnull": False,
        "document_type": 1,
        "due_date__isnull": False,
        "is_posted": True,
    }


class LedgerViewSet(viewsets.ViewSet):
    start_date = end_date = None

    def init_date(self):
        self.start_date = (
            datetime.strptime(self.request.GET["start_date"], "%d-%m-%Y").date()
            if self.request.GET.get("start_date")
            else None
        )
        self.end_date = (
            datetime.strptime(self.request.GET["end_date"], "%d-%m-%Y").date()
            if self.request.GET.get("end_date")
            else None
        )

        if not self.start_date and not self.end_date:
            self.start_date = datetime.now()

    def get_filtered_queryset(self, qs):
        if self.start_date and self.end_date:
            qs = qs.filter(
                journal__posted_date__gte=self.start_date,
                journal__posted_date__lte=self.end_date,
            )
        else:
            qs = qs.filter(journal__posted_date__gte=self.start_date)
        return qs.order_by("journal__posted_date")

    def retrieve(self, request, pk=None):
        self.init_date()
        account = get_object_or_404(
            Account, organization_id=request.user.organization_id, pk=pk
        )
        assert account.is_active, "Only active account has ledger"
        posted_transactions = Transaction.objects.filter(
            account=account, journal__is_posted=True
        )

        def balance(b):
            return b * account.balance_type

        def opening_balance():
            t = posted_transactions.filter(
                journal__posted_date__lt=self.start_date
            ).aggregate(
                debit=Coalesce(Sum("debit"), 0), credit=Coalesce(Sum("credit"), 0)
            )
            return balance(t["debit"] - t["credit"])

        opening_balance = opening_balance()
        transactions = self.get_filtered_queryset(posted_transactions)
        serializer = serializers.LedgerSerializer(transactions, many=True)

        closing_balance = opening_balance
        for row in serializer.data:
            closing_balance += balance(Decimal(row["debit"]) - Decimal(row["credit"]))
            row["balance"] = closing_balance

        return Response(
            {
                "transactions": serializer.data,
                "opening_balance": opening_balance,
                "closing_balance": closing_balance,
            }
        )


class TrialBalanceView(viewsets.ViewSet):
    def list(self, request):
        start_date = (
            datetime.strptime(request.GET["start_date"], "%d-%m-%Y").date()
            if request.GET.get("start_date")
            else None
        )
        end_date = (
            datetime.strptime(request.GET["end_date"], "%d-%m-%Y").date()
            if request.GET.get("end_date")
            else None
        )

        if not start_date and not end_date:
            start_date = datetime.now()

        values = ["account", "account__code", "account__name", "account__balance_type"]
        d = {
            "organization_id": self.request.user.organization_id,
            "journal__is_posted": True,
        }
        t = (
            Transaction.objects.filter(journal__posted_date__lt=start_date, **d)
            .values(*values)
            .annotate(
                debit=Coalesce(Sum("debit"), 0), credit=Coalesce(Sum("credit"), 0)
            )
        )

        balance = {
            a["account"]: (a["debit"] - a["credit"]) * a["account__balance_type"]
            for a in t
        }

        if start_date and end_date:
            transactions = (
                Transaction.objects.filter(
                    journal__posted_date__gte=start_date,
                    journal__posted_date__lte=end_date,
                    **d
                )
                .values(*values)
                .annotate(
                    debit=Coalesce(Sum("debit"), 0), credit=Coalesce(Sum("credit"), 0)
                )
                .order_by("account__code")
            )

        else:
            transactions = (
                Transaction.objects.filter(journal__posted_date__gte=start_date, **d)
                .values(*values)
                .annotate(
                    debit=Coalesce(Sum("debit"), 0), credit=Coalesce(Sum("credit"), 0)
                )
                .order_by("account__code")
            )
        # paginator = LimitOffsetPagination()
        # transactions = paginator.paginate_queryset(transactions, request)
        for t in transactions:
            try:
                t["opening_balance"] = balance[t["account"]]
            except KeyError:
                t["opening_balance"] = 0

            t["closing_balance"] = (
                t["opening_balance"]
                + (t["debit"] - t["credit"]) * t["account__balance_type"]
            )

        return Response(transactions)


class BaseStatementView(viewsets.ViewSet):
    start_date = end_date = None

    def init_date(self, request):
        start = request.GET.get("start_date", None)
        end = request.GET.get("end_date", None)
        self.start_date = datetime.strptime(start, "%d-%m-%Y").date() if start else None
        self.end_date = datetime.strptime(end, "%d-%m-%Y").date() if end else None

        if not self.start_date and not self.end_date:
            self.start_date = datetime.now()

    def get_response(self, data):
        pass

    def get_filtered_accounts(self, group_range):
        d = {
            "organization_id": self.request.user.organization_id,
            "group_id__in": group_range,
            "transactions__journal__is_posted": True,
        }

        if self.start_date and self.end_date:
            accounts = Account.objects.filter(
                transactions__journal__posted_date__gte=self.start_date,
                transactions__journal__posted_date__lte=self.end_date,
                **d
            )
        else:
            accounts = Account.objects.filter(
                transactions__journal__posted_date__lte=self.start_date, **d
            )
        return accounts.select_related("organization", "group")

    def get_filtered_transactions(self, group_range):
        d = {
            "journal__organization_id": self.request.user.organization_id,
            "account__group_id__in": group_range,
            "journal__is_posted": True,
            "account__is_active": True,
        }

        if self.start_date and self.end_date:
            transactions = Transaction.objects.filter(
                journal__posted_date__gte=self.start_date,
                journal__posted_date__lte=self.end_date,
                **d
            )
        else:
            transactions = Transaction.objects.filter(
                journal__posted_date__lte=self.start_date, **d
            )
        return transactions.values(
            "account", "account__balance_type", "account__group_id"
        ).annotate(bal=Sum(F("debit") - F("credit")))

    def list(self, request):
        self.init_date(request)

        trans = self.get_filtered_transactions(self.group_range)
        balances = {t["account"]: t["bal"] * t["account__balance_type"] for t in trans}

        accounts = Account.objects.filter(
            organization_id=self.request.user.organization_id,
            group_id__in=self.group_range,
        ).select_related("group")

        serializer = serializers.StatementSerializer(
            accounts.filter(parent=None).prefetch_related("children"), many=True
        )

        def reform_data(data):
            data["children"] = [x for x in data["children"]]
            if not data["children"]:
                try:
                    data["balance"] = balances[data["id"]]
                except KeyError:
                    data["balance"] = 0
            else:
                for a in data["children"]:
                    reform_data(a)
                data["balance"] = 0  # sum(b['balance'] for b in data['children'])

        serializer_data = [a for a in serializer.data]
        for a in serializer_data:
            reform_data(a)

        resp = self.get_response(serializer.data)

        return Response(resp)


class IncomeStatementView(BaseStatementView):
    group_range = list(range(15, 26))

    def get_response(self, data):
        resp = {}
        for key, group in groupby(
            sorted(data, key=lambda x: x["group_code"]), lambda x: x["group_code"]
        ):
            resp[key] = list(group)

        group_dict = OrderedDict(
            [
                (15, "Revenue"),
                (18, "Cost of Goods Sold"),
                (19, "Direct Labor"),
                (20, "Direct Overhead"),
                (16, "Other Operating Income"),
                (21, "Administrative Expense"),
                (22, "Selling Expense"),
                (17, "Non operating Income"),
                (23, "Non operating Expense"),
                (24, "Income Tax"),
            ]
        )

        resp_data = list()
        for g in group_dict.items():
            d = dict()
            d["name"] = g[1]
            d["code"] = g[0]
            d["balance"] = 0
            try:
                d["children"] = resp[str(g[0])]
            except Exception:
                d["children"] = []
            resp_data.append(d)
        return resp_data


class BalanceSheetView(BaseStatementView):
    group_range = list(range(1, 15))

    def get_response(self, data):
        resp = {}
        for key, group in groupby(
            sorted(data, key=lambda x: x["category"]), lambda x: x["category"]
        ):
            l = []
            for k, g in groupby(
                sorted(group, key=lambda x: x["group_code"]), lambda x: x["group_name"]
            ):
                l.append({"name": k, "children": list(g), "balance": 0})
            resp[key] = l

        group_dict = OrderedDict(
            [
                (0, "Current Assets"),
                (1, "Non-current Assets"),
                (2, "Current Liabilities"),
                (3, "Non-current Liabilities"),
                (4, "Equity"),
            ]
        )

        resp_data = list()

        for g in group_dict.items():
            d = dict()
            d["name"] = g[1]
            d["balance"] = 0
            d["code"] = g[0]
            try:
                d["children"] = resp[str(g[0])]
            except Exception as e:
                d["children"] = []

            # Add retained earnings under equity category
            if g[0] == 4:
                d["children"].append(
                    {
                        "name": "Retained Earnings",
                        "balance": self.get_net_income(),
                        "children": [],
                    }
                )
            resp_data.append(d)

        return resp_data

    def get_net_income(self):
        trans = self.get_filtered_transactions(list(range(15, 26)))
        earnings = 0

        def is_positive_revenue_account(t):
            return (
                t["account__group_id"] in [15, 16, 17]
                and t["account__balance_type"] == -1
            )

        for t in trans:
            balance_type = t["account__balance_type"]
            balance = t["bal"] * balance_type
            earnings += balance if is_positive_revenue_account(t) else -1 * balance

        return earnings


class CashFlowView(BalanceSheetView):
    group_range = list(range(1, 27))

    def get_response(self, data):
        resp = {}
        for key, group in groupby(
            sorted(data, key=lambda x: x["group_code"]), lambda x: x["group_code"]
        ):
            resp[key] = list(group)

        group_dict = OrderedDict(
            [
                (2, "Account Receivable"),
                (3, "Inventory"),
                (4, "Other Current Assets"),
                (8, "Account Payable"),
                (10, "Other Current Liabilities"),
                (5, "Fixed Asset"),
                (6, "Accumulated Depreciation"),
                (7, "Other Non-current Assets"),
                (11, "Long Term Liabilities"),
                (13, "Share Capital"),
                (14, "Shareholder's Equity"),
            ]
        )

        activities = [
            "Operating Activities",
            "Investing Activities",
            "Financing Activities",
            "Cash & Cash Equivalent at Beginning of {}".format(
                self.start_date.date()
                if isinstance(self.start_date, datetime)
                else self.start_date
            ),
        ]

        resp_data = list()
        for i, a in enumerate(activities):
            l = dict()
            l["code"] = 0
            l["name"] = a
            l["children"] = (
                [
                    {
                        "name": "Net Income",
                        "balance": self.get_net_income(),
                        "children": [],
                    },
                    {"name": "Adjustments", "balance": 0, "children": []},
                ]
                if i == 0
                else []
            )
            l["balance"] = 0
            resp_data.append(l)

        for g in group_dict.items():
            d = dict()
            d["name"] = g[1]
            d["code"] = g[0]
            d["balance"] = 0
            try:
                d["children"] = resp[str(g[0])]
            except Exception as e:
                d["children"] = []

            if g[0] in [2, 3, 4, 8, 10]:
                resp_data[0]["children"][1]["children"].append(d)
            elif g[0] in [5, 6, 7, 11]:
                resp_data[1]["children"].append(d)
            elif g[0] in [13, 14]:
                resp_data[2]["children"].append(d)
        return resp_data

    def get_cash_and_cash_equivalent(self):
        accounts = (
            self.get_filtered_accounts([1])
            .values("group")
            .annotate(
                bal=Case(
                    When(
                        balance_type=1,
                        then=Coalesce(
                            Sum(F("transactions__debit") - F("transactions__credit")), 0
                        ),
                    ),
                    When(
                        balance_type=-1,
                        then=Coalesce(
                            Sum(F("transactions__credit") - F("transactions__debit")), 0
                        ),
                    ),
                )
            )
        )

        return sum(a["bal"] for a in accounts)


class VoucherView(viewsets.ViewSet):
    def list(self, request):
        """
        :return: Credit Voucher for collection from student, Debit Voucher for payment to teacher, Journal voucher for
         Non cash transaction
        """

        payment_id = self.request.GET.get("payment_id", None)
        journal_id = self.request.GET.get("journal_id", None)
        invoice_id = self.request.GET.get("invoice_id", None)
        if payment_id:
            d = {"payment_id": payment_id}
        elif invoice_id:
            d = {"invoice_id": invoice_id}
        else:
            d = {"id": journal_id}

        journal = get_object_or_404(Journal, **d)
        if journal.is_posted:
            return Response(VoucherSerializer(journal).data)
        else:
            return Response({"message": "No voucher has been created yet"})


class DashBoardView(viewsets.ViewSet):
    def list(self, request):
        organization_id = self.request.user.organization_id

        invoice_entries = Invoice.objects.filter(
            organization_id=organization_id,
            document_type__in=[0, 1],
            due_date__isnull=False,
            due_date__gte=datetime.today(),
            due_date__lte=datetime.today() + timedelta(days=7),
        ).values("number", "due_date")
        pending_invoices = invoice_entries.filter(document_type=0)
        pending_bills = invoice_entries.filter(document_type=1)
        today = datetime.today().date()
        one_month_later = today + timedelta(days=31)
        renew_date = request.user.organization.trade_license_renew_time
        if renew_date is not None:
            is_trade_license_renewable = (
                today <= renew_date <= one_month_later or renew_date <= today
            )
        else:
            is_trade_license_renewable = False

        return Response(
            {
                "pending_invoices": pending_invoices,
                "pending_bills": pending_bills,
                "renew_trade_license": {
                    "status": is_trade_license_renewable,
                    "date": renew_date,
                },
            }
        )


class BaseEntryReport(BaseViewSet):
    http_method_names = ["get"]
    pagination_class = None
    start_date = end_date = None
    document_type = None

    def init_date(self, request):
        start = request.GET.get("start_date", None)
        end = request.GET.get("end_date", None)
        self.start_date = datetime.strptime(start, "%d-%m-%Y").date() if start else None
        self.end_date = datetime.strptime(end, "%d-%m-%Y").date() if end else None

        if not self.start_date and not self.end_date:
            self.start_date = datetime.now()

    def get_filtered_queryset(self, qs):
        if self.start_date and self.end_date:
            qs = qs.filter(
                posted_date__gte=self.start_date, posted_date__lte=self.end_date
            )
        else:
            qs = qs.filter(posted_date__lte=self.start_date)
        return qs

    def get_queryset(self):
        self.init_date(self.request)
        self.document_type = self.document_dict.get(
            self.request.GET.get("document_type"), None
        )
        qs = super().get_queryset()
        if self.document_type is not None:
            qs = self.get_filtered_queryset(
                qs.filter(**{self.filter: self.document_type})
            )

        student_id = self.request.GET.get("student_id", None)
        teacher_id = self.request.GET.get("teacher_id", None)
        sales_person_id = self.request.GET.get("sales_person_id", None)
        if student_id:
            qs = qs.filter(student_id=student_id)
        if teacher_id:
            qs = qs.filter(teacher_id=teacher_id)
        if sales_person_id:
            qs = qs.filter(sales_person_id=sales_person_id)

        return qs

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            "request": self.request,
            "format": self.format_kwarg,
            "view": self,
            "document_type": self.document_type,
        }


class InvoiceReport(BaseEntryReport):
    # TODO: change this raw query to ORM/SubQuery
    queryset = (
        Invoice.objects.filter(is_posted=True)
        .select_related("teacher", "student", "sales_person")
        .prefetch_related("payments")
    )
    serializer_class = InvoiceReportSerializer
    document_dict = {"invoice": 0, "billing": 1, "credit_note": 2, "debit_note": 3}
    filter = "document_type"


class PaymentReport(BaseEntryReport):
    queryset = (
        Payment.objects.filter(is_posted=True)
        .select_related("teacher", "student")
        .annotate(amount=Sum("net_amount"), total_discount=Sum("discount"))
    )
    serializer_class = PaymentReportSerializer
    document_dict = {"collection": 0, "payment": 1}
    filter = "type"

    def get_queryset(self):
        qs = super().get_queryset()
        payment_account_id = self.request.GET.get("payment_account_id", None)
        if payment_account_id:
            qs = qs.filter(payment_account_id=payment_account_id)
        return qs


class JournalEntryReport(BaseEntryReport):
    queryset = (
        Journal.objects.filter(is_posted=True)
        .select_related("organization", "invoice", "payment")
        .prefetch_related("transactions", "transactions__account")
        .annotate(debit=Sum("transactions__debit"), credit=Sum("transactions__credit"))
    )
    serializer_class = JournalEntryReportSerializer

    def get_queryset(self):
        self.init_date(self.request)
        qs = super(BaseViewSet, self).get_queryset()
        qs = self.get_filtered_queryset(qs)

        return qs
