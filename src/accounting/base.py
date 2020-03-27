from django.db import transaction
from django.db.models import Q

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
import logging

from src.accounting.utils import create_initial_accounts
from src.api.v1.permissions import AuxiliaryModelPermission
from src.api.v1.viewsets import BaseViewSet
from src.accounting.utils import validate_accounting_equation
from src.organization.models import Counter
from .models import (
    Transaction,
    Journal,
    Invoice,
    Payment,
    Account,
)
from . import serializers

console = logging.getLogger("console")
error_logger = logging.getLogger("accounting.error")
warning_logger = logging.getLogger("accounting.warning")


class BaseJournalViewSet(BaseViewSet):
    queryset = Journal.objects.all().prefetch_related(
        "transactions", "transactions__account"
    )
    serializer_class = serializers.JournalSerializer
    batch = None
    entry = None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if self.batch and self.entry:
            serializer = self.get_serializer(queryset, many=True)
            try:
                data = serializer.data[0]
            except Exception as e:
                data = {}

            return Response(data)

        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def get_queryset(self):
        self.entry = int(self.request.GET.get("entry", 0))
        qs = super().get_queryset().order_by("id")

        if self.batch:
            qs = qs.filter(batch_id=self.batch)
        if self.entry:
            qs = qs[self.entry - 1 : self.entry]

        return qs

    def perform_create(self, serializer):
        transactions = serializer.validated_data.pop("transactions")

        if not validate_accounting_equation(transactions):
            error_logger.error("Error in accounting equation")
            raise ValidationError("Error in accounting equation")

        with transaction.atomic():
            counter = Counter.objects.select_for_update().get(
                organization_id=self.get_organization_id()
            )
            serializer.validated_data.update({"number": counter.next_journal_number()})
            instance = super().perform_create(serializer)
            for t in transactions:
                Transaction.objects.create(
                    organization_id=self.get_organization_id(), journal=instance, **t
                )
            counter.save()

    def perform_update(self, serializer):
        transactions = serializer.validated_data.pop("transactions")

        if not transactions:
            raise ValidationError("You must enter journal items")
        if not validate_accounting_equation(transactions):
            error_logger.error("Error in accounting equation")
            raise ValidationError("Error in accounting equation")

        with transaction.atomic():
            instance = super().perform_update(serializer)
            for t in transactions:
                t_id = t.get("id", None)
                if t_id:
                    Transaction.objects.filter(id=t_id).update(**t)
                else:
                    Transaction.objects.create(
                        organization_id=self.get_organization_id(),
                        journal=instance,
                        **t
                    )


class BaseInvoiceViewSet(BaseViewSet):
    queryset = (
        Invoice.objects.all()
        .prefetch_related("transactions", "transactions__account")
        .select_related("vendor", "customer", "sales_person")
    )
    batch = None
    entry = None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if self.batch and self.entry:
            serializer = self.get_serializer(queryset, many=True)
            try:
                data = serializer.data[0]
            except Exception as e:
                data = {}

            return Response(data)

        else:
            # page = self.paginate_queryset(queryset)
            # if page is not None:
            #     serializer = self.get_serializer(page, many=True)
            #     return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def get_queryset(self):
        self.batch = self.request.GET.get("batch")
        self.entry = int(self.request.GET.get("entry", 0))
        qs = (
            super()
            .get_queryset()
            .filter(document_type=self.document_type)
            .order_by("id")
        )

        if self.batch:
            qs = qs.filter(batch_id=self.batch)
        if self.entry:
            qs = qs[self.entry - 1 : self.entry]

        return qs

    def get_next_document_number(self, counter):
        return {
            0: counter.next_invoice_number(),
            1: counter.next_billing_number(),
            2: counter.next_credit_note_number(),
            3: counter.next_debit_note_number(),
        }[self.document_type]

    def perform_create(self, serializer):
        with transaction.atomic():
            counter = Counter.objects.get(organization_id=self.get_organization_id())
            serializer.validated_data.update(
                {
                    "number": self.get_next_document_number(counter),
                    "document_type": self.document_type,
                }
            )
            instance = super().perform_create(serializer)
            instance.calculate_net_amount()
            instance.save()
            counter.save()

    def perform_update(self, serializer):
        transactions = serializer.validated_data.pop("transactions")
        if not transactions:
            raise ValidationError("You must enter items inside each entry")

        instance = super().perform_update(serializer)
        instance.calculate_net_amount()
        instance.save()


class BasePaymentViewSet(BaseViewSet):
    queryset = Payment.objects.all().prefetch_related("transactions")
    permission_classes = BaseViewSet.permission_classes + (AuxiliaryModelPermission,)
    auxiliary_model = Payment
    batch = None
    entry = None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if self.batch and self.entry:
            serializer = self.get_serializer(queryset, many=True)
            try:
                data = serializer.data[0]
            except Exception as e:
                data = {}

            return Response(data)

        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def get_queryset(self):
        self.batch = self.request.GET.get("batch")
        self.entry = int(self.request.GET.get("entry", 0))
        qs = super().get_queryset().filter(type=self.type).order_by("id")

        if self.batch:
            qs = qs.filter(batch_id=self.batch)
        if self.entry:
            qs = qs[self.entry - 1 : self.entry]

        return qs

    def get_next_number(self, counter):
        return {0: counter.next_collection_number(), 1: counter.next_payment_number()}[
            self.type
        ]

    def perform_create(self, serializer):
        transactions = serializer.validated_data.pop("transactions")
        if not transactions:
            raise ValidationError("You must have at least 1 transaction")

        with transaction.atomic():
            counter = Counter.objects.select_for_update().get(
                organization_id=self.get_organization_id()
            )
            serializer.validated_data.update(
                {"number": self.get_next_number(counter), "type": self.type}
            )
            instance = super().perform_create(serializer)
            for t in transactions:
                if t["amount"] <= 0:
                    raise ValidationError("You must enter amount greater than 0")
                Payment.objects.create(
                    organization_id=self.get_organization_id(), payment=instance, **t
                )

            counter.save()

    def perform_update(self, serializer):
        transactions = serializer.validated_data.pop("transactions")
        if not transactions:
            raise ValidationError("You must have at least 1 transaction")

        with transaction.atomic():
            instance = super().perform_update(serializer)
            # delete all unchecked transactions if previously checked
            checked_transactions = [t["id"] for t in transactions if t.get("id")]
            instance.transactions.exclude(id__in=checked_transactions).delete()

            for t in transactions:
                if t["amount"] <= 0 or t["discount"] < 0:
                    raise ValidationError("You must enter amount greater than 0")
                t_id = t.get("id", None)

                if t_id:
                    Payment.objects.filter(id=t_id).update(**t)
                else:
                    Payment.objects.create(
                        organization_id=self.get_organization_id(),
                        payment=instance,
                        **t
                    )


class DueEntryView(BaseViewSet):
    queryset = Invoice.objects.filter(is_posted=True).prefetch_related("payments")
    http_method_names = ["get"]
    pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset().filter(document_type__in=self.document_type)

        customer_id = self.request.GET.get("customer_id", None)
        vendor_id = self.request.GET.get("vendor_id", None)

        if customer_id:
            qs = qs.filter(customer_id=customer_id)
        elif vendor_id:
            qs = qs.filter(vendor_id=vendor_id)

        return qs

    @staticmethod
    def _exclude_totally_paid_invoices(queryset):
        return [q for q in queryset if q.bill != (q.paid + q.discount)]

    def list(self, request, *args, **kwargs):
        """ 
        :return: 1. Posted due invoices only for customer/vendor selected. 
                 2. If any payment to any invoices of payment_id, these invoices will be marked as applied and applied
                    amount will be sent.
        """
        payment_id = self.request.GET.get("payment_id", None)
        queryset = self.filter_queryset(self.get_queryset())
        queryset = self._exclude_totally_paid_invoices(queryset)
        serializer = self.get_serializer(queryset, many=True)

        applied_transactions = Payment.objects.filter(payment_id=payment_id).only(
            "id", "invoice_id", "amount", "discount"
        )
        # {invoice_id: [payment_id, amount]} format
        applied = {
            t.invoice_id: [t.id, t.amount, t.discount] for t in applied_transactions
        }

        for d in serializer.data:
            try:
                applied_id = applied[d["id"]]
                d["applied_amount"] = applied_id[1]
                d["applied"] = True
                d["payment_id"] = applied_id[0]
                d["discount"] = applied_id[2]
            except KeyError:
                d["applied_amount"] = 0
                d["applied"] = False
                d["discount"] = 0

        return Response(serializer.data)


def clone_accounts_from_organization_to_branch(organization, branch):
    if branch.get_level() == 1:
        create_initial_accounts(branch.id)
    if organization.get_level() == 1 and branch.parent == organization:
        accounts = Account.objects.filter(organization=organization)
        branch_accounts = []

        for a in accounts:
            a.pk = None
            a.organization_id = branch.id
            branch_accounts.append(a)

        Account.objects.bulk_create(branch_accounts)
