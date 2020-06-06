from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from src.accounting.models import (
    AccountGroup,
    Account,
    Transaction,
    Journal,
    Invoice,
    Payment,
)
from src.api.v1.validators import UniqueTogetherFieldValidator


class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    account_text = SerializerMethodField()

    class Meta:
        model = Transaction
        exclude = ["last_updated", "organization", "journal", "type", "amount"]
        read_only_fields = ["date_created", "is_deleted", "posted_date", "entry"]

    def get_account_text(self, ob):
        return "{} ({})".format(ob.account.name, ob.account.code)


class AccountSerializer(serializers.ModelSerializer):
    group_text = SerializerMethodField()
    balance_type_text = SerializerMethodField()

    class Meta:
        model = Account
        exclude = ["date_created", "last_updated"]
        validators = [
            UniqueTogetherFieldValidator(
                queryset=Account.objects.all(),
                fields=("organization", "name"),
                message="This name is already used. Try another, please.",
            )
        ]

    def get_group_text(self, ob):
        return ob.group.name

    def get_balance_type_text(self, ob):
        return ob.get_balance_type_display()


class AccountGroupSerializer(serializers.ModelSerializer):
    category_text = SerializerMethodField()

    class Meta:
        model = AccountGroup
        fields = "__all__"

    def get_category_text(self, ob):
        return ob.get_category_display()


class JournalSerializer(serializers.ModelSerializer):
    trans = TransactionSerializer(source="transactions", many=True)

    class Meta:
        model = Journal
        exclude = ["last_updated", "organization"]
        read_only_fields = ["date_created", "approved"]

    def validate(self, data):
        if data["posted_date"] is None:
            raise serializers.ValidationError("you must enter posted date")
        return data


class JournalEntryReportSerializer(JournalSerializer):
    number = SerializerMethodField()
    debit = SerializerMethodField()
    credit = SerializerMethodField()
    document_date = SerializerMethodField()

    class Meta(JournalSerializer.Meta):
        exclude = JournalSerializer.Meta.exclude + [
            "is_deleted",
            "is_posted",
            "approved",
            "date_created",
        ]

    def get_number(self, ob):
        if ob.invoice:
            number = {0: "INV", 1: "BILL", 2: "CN", 3: "DN"}[
                ob.invoice.document_type
            ] + "-{}".format(ob.invoice.number)

        elif ob.payment:
            number = {0: "COLLECTION", 1: "PAYMENT"}[ob.payment.type] + "-{}".format(
                ob.payment.number
            )
        else:
            number = "JOURNAL-{}".format(ob.number)
        return number

    def get_debit(self, ob):
        return ob.debit

    def get_credit(self, ob):
        return ob.credit

    def get_document_date(self, ob):
        if ob.invoice:
            date = ob.invoice.document_date
        elif ob.payment:
            date = ob.payment.document_date
        else:
            date = ob.document_date
        return date


class BaseInvoiceSerializer(serializers.ModelSerializer):
    number = SerializerMethodField()
    document_type_text = SerializerMethodField()

    class Meta:
        model = Invoice
        exclude = [
            "last_updated",
            "organization",
        ]
        read_only_fields = [
            "date_created",
            "approved",
            "is_deleted",
            "number",
            "document_type",
            "is_posted",
        ]

    def get_number(self, ob):
        text = {0: "INV", 1: "BILL", 2: "CN", 3: "DN"}[ob.document_type]
        return text + "-{}".format(ob.number)

    def get_document_type_text(self, ob):
        return ob.get_document_type_display()

    def validate(self, data):
        if data["posted_date"] is None:
            raise serializers.ValidationError("You must enter posted date")
        return data


class InvoiceReportSerializer(BaseInvoiceSerializer):
    student_text = SerializerMethodField()
    teacher_text = SerializerMethodField()
    net_amount = SerializerMethodField()
    paid_amount = SerializerMethodField()
    due_amount = SerializerMethodField()

    class Meta(BaseInvoiceSerializer.Meta):
        exclude = BaseInvoiceSerializer.Meta.exclude + [
            "is_deleted",
            "is_posted",
            "date_created",
            "approved",
        ]

    def get_student_text(self, ob):
        return "{}-({})".format(ob.student.name, ob.student.code) if ob.student else ""

    def get_teacher_text(self, ob):
        return "{}-{}".format(ob.teacher.code, ob.teacher.name) if ob.teacher else ""

    def get_net_amount(self, ob):
        return ob.bill

    def get_paid_amount(self, ob):
        return ob.paid

    def get_due_amount(self, ob):
        return ob.bill - ob.paid


class InvoiceSerializer(BaseInvoiceSerializer):
    student_text = SerializerMethodField()

    class Meta(BaseInvoiceSerializer.Meta):
        exclude = BaseInvoiceSerializer.Meta.exclude + ["teacher"]

    def get_student_text(self, ob):
        return "{}-({})".format(ob.student.name, ob.student.code)

    def validate(self, data):
        if data["due_date"] is None:
            raise serializers.ValidationError("You must enter due date")
        elif data["posted_date"] and data["posted_date"] > data["due_date"]:
            raise serializers.ValidationError(
                "Posted date must be before than due date"
            )
        return super().validate(data)


class CreditNoteEntrySerializer(BaseInvoiceSerializer):
    student_text = SerializerMethodField()

    class Meta(BaseInvoiceSerializer.Meta):
        exclude = BaseInvoiceSerializer.Meta.exclude + [
            "teacher",
            "due_date",
        ]

    def get_student_text(self, ob):
        return "{}-({})".format(ob.student.name, ob.student.code)


class BillingEntrySerializer(BaseInvoiceSerializer):
    teacher_text = SerializerMethodField()

    class Meta(BaseInvoiceSerializer.Meta):
        exclude = BaseInvoiceSerializer.Meta.exclude + ["student"]

    def get_teacher_text(self, ob):
        return "{}-{}".format(ob.teacher.code, ob.teacher.name)

    def validate(self, data):
        if data["due_date"] is None:
            raise serializers.ValidationError("You must enter due date")
        elif data["posted_date"] and data["posted_date"] > data["due_date"]:
            raise serializers.ValidationError(
                "Posted date must be before than due date"
            )
        return super().validate(data)


class DebitNoteEntrySerializer(BaseInvoiceSerializer):
    teacher_text = SerializerMethodField()

    class Meta(BaseInvoiceSerializer.Meta):
        exclude = BaseInvoiceSerializer.Meta.exclude + [
            "student",
            "due_date",
        ]

    def get_teacher_text(self, ob):
        return "{}-{}".format(ob.teacher.code, ob.teacher.name)


class DueInvoiceSerializer(InvoiceSerializer):
    student_text = None
    due_amount = SerializerMethodField()
    applied_amount = SerializerMethodField()
    payment_number = SerializerMethodField()
    total_bill_amount = SerializerMethodField()
    discount = SerializerMethodField()

    class Meta(InvoiceSerializer.Meta):
        exclude = InvoiceSerializer.Meta.exclude + ["student", "is_deleted", "approved"]

    def get_due_amount(self, ob):
        return ob.bill - ob.paid - ob.discount

    def get_applied_amount(self, ob):
        return ob.paid

    def get_payment_number(self, ob):
        return ob.payment_number

    def get_total_bill_amount(self, ob):
        return ob.bill

    def get_discount(self, ob):
        return ob.discount


class DueBillingEntrySerializer(BillingEntrySerializer):
    teacher_text = None
    due_amount = SerializerMethodField()
    applied_amount = SerializerMethodField()
    payment_number = SerializerMethodField()
    total_bill_amount = SerializerMethodField()

    class Meta(BillingEntrySerializer.Meta):
        exclude = BillingEntrySerializer.Meta.exclude + [
            "teacher",
            "is_deleted",
            "approved",
        ]

    def get_due_amount(self, ob):
        return ob.bill - ob.paid

    def get_applied_amount(self, ob):
        return ob.paid

    def get_payment_number(self, ob):
        return ob.payment_number

    def get_total_bill_amount(self, ob):
        return ob.bill


class BasePaymentSerializer(serializers.ModelSerializer):
    number = SerializerMethodField()
    payment_account_text = SerializerMethodField()

    class Meta:
        model = Payment
        exclude = ["last_updated", "organization"]
        read_only_fields = [
            "date_created",
            "approved",
            "is_deleted",
            "number",
            "type",
            "is_posted",
        ]

    def get_payment_account_text(self, ob):
        return "{} ({})".format(ob.payment_account.name, ob.payment_account.code)

    def get_number(self, ob):
        return {0: "COLLECTION", 1: "PAYMENT"}[ob.type] + "-{}".format(ob.number)


class PaymentReportSerializer(BasePaymentSerializer):
    amount = SerializerMethodField()
    discount = SerializerMethodField()
    student_text = SerializerMethodField()
    teacher_text = SerializerMethodField()

    class Meta(BasePaymentSerializer.Meta):
        exclude = BasePaymentSerializer.Meta.exclude + [
            "date_created",
            "type",
            "approved",
            "is_deleted",
            "is_posted",
        ]

    def get_amount(self, ob):
        return ob.amount

    def get_discount(self, ob):
        return ob.discount

    def get_student_text(self, ob):
        return (
            "{} ({})".format(ob.student.name, ob.student.code) if ob.student else None
        )

    def get_teacher_text(self, ob):
        return (
            "{} ({})".format(ob.teacher.name, ob.teacher.code) if ob.teacher else None
        )


class CollectionEntrySerializer(BasePaymentSerializer):
    student_text = SerializerMethodField()

    class Meta(BasePaymentSerializer.Meta):
        exclude = BasePaymentSerializer.Meta.exclude + ["teacher"]

    def get_student_text(self, ob):
        return "{} ({})".format(ob.student.name, ob.student.code)


class PaymentSerializer(BasePaymentSerializer):
    teacher_text = SerializerMethodField()

    class Meta(BasePaymentSerializer.Meta):
        exclude = BasePaymentSerializer.Meta.exclude + ["student"]

    def get_teacher_text(self, ob):
        return "{} ({})".format(ob.teacher.name, ob.teacher.code)


#
# course AccountSerializer(serializers.ModelSerializer):
#     course Meta:
#         model = Account
#         exclude = ["date_created", "last_updated"]


class COASerializer(serializers.ModelSerializer):
    group_text = SerializerMethodField()
    balance_type_text = SerializerMethodField()
    account_type_text = SerializerMethodField()

    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = ["date_created", "organization"]
        validators = [
            UniqueTogetherFieldValidator(
                queryset=Account.objects.all(),
                fields=("organization", "name"),
                message="This name is already used. Try another, please.",
            )
        ]

    def get_group_text(self, ob):
        return ob.group.name

    def get_balance_type_text(self, ob):
        return ob.get_balance_type_display()

    def get_account_type_text(self, ob):
        return ob.get_account_type_display()


class LedgerSerializer(serializers.ModelSerializer):
    date = SerializerMethodField()
    reference = SerializerMethodField()
    invoice_id = serializers.PrimaryKeyRelatedField(
        source="journal.invoice", read_only=True
    )
    payment_id = serializers.PrimaryKeyRelatedField(
        source="journal.payment", read_only=True
    )
    journal_id = serializers.PrimaryKeyRelatedField(source="journal", read_only=True)
    detail = SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "date",
            "detail",
            "reference",
            "debit",
            "credit",
            "invoice_id",
            "payment_id",
            "journal_id",
        ]

    def get_date(self, ob):
        return ob.journal.posted_date

    def get_reference(self, ob):
        if ob.journal.invoice:
            number = {0: "INV", 1: "BILL", 2: "CN", 3: "DN"}[
                ob.journal.invoice.document_type
            ] + "-{}".format(ob.journal.invoice.number)

        elif ob.journal.payment:
            number = {0: "COLLECTION", 1: "PAYMENT"}[
                ob.journal.payment.type
            ] + "-{}".format(ob.journal.payment.number)
        else:
            number = "JOURNAL-{}".format(ob.journal.number)
        return number

    def get_detail(self, ob):
        if ob.journal.invoice:
            return ob.journal.invoice.description
        elif ob.journal.payment:
            return ob.journal.payment.description
        else:
            return ob.journal.description


class StatementSerializer(serializers.ModelSerializer):
    group_code = serializers.StringRelatedField(source="group.code")
    group_name = serializers.StringRelatedField(source="group.name")
    category = serializers.StringRelatedField(source="group.category")

    class Meta:
        model = Account
        fields = ["id", "code", "name", "group_code", "category", "group_name", "level"]

    def get_fields(self):
        fields = super().get_fields()
        fields["children"] = StatementSerializer(many=True, read_only=True)
        return fields


class VoucherTransactionSerializer(TransactionSerializer):
    account_code = serializers.StringRelatedField(source="account.code")
    account_name = serializers.StringRelatedField(source="account.name")

    class Meta:
        model = Transaction
        fields = ["account_code", "account_name", "debit", "credit"]


class VoucherSerializer(serializers.ModelSerializer):
    organization_name = serializers.StringRelatedField(source="organization.name")
    organization_address = serializers.StringRelatedField(source="organization.address")
    voucher_type = serializers.SerializerMethodField()
    voucher_number = serializers.SerializerMethodField()

    transactions = VoucherTransactionSerializer(many=True)
    narration = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    payment_mode = serializers.SerializerMethodField()

    class Meta:
        model = Journal
        fields = [
            "organization_name",
            "organization_address",
            "voucher_type",
            "voucher_number",
            "date",
            "transactions",
            "narration",
            "payment_mode",
            "prepared_by",
            "approved_by",
        ]

    def get_voucher_type(self, ob):
        return {0: "Credit Voucher", 1: "Debit Voucher"}.get(
            ob.payment.type if ob.payment else None, "Journal Voucher"
        )

    def get_voucher_number(self, ob):
        d = {0: "CV/", 1: "DV/"}.get(ob.payment.type if ob.payment else None, "JV/")

        return "{}{}".format(d, ob.payment.number if ob.payment else ob.number)

    def get_date(self, ob):
        return ob.posted_date

    def get_narration(self, ob):
        return ob.payment.description if ob.payment else ob.description

    def get_payment_mode(self, ob):
        return ob.payment.payment_account.name if ob.payment else ""
