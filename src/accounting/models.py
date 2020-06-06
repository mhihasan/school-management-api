from datetime import datetime
from decimal import Decimal

from django.db import models
from django.db.models import Sum, F, Index
from django.db.models.functions import Coalesce

from src.accounting.constants import (
    ACCOUNT_GROUP_TYPE,
    ACCOUNT_TYPE,
    DOC_TYPE,
    PAYMENT_TYPE,
    PAYMENT_MODE,
    TRANSACTION_TYPE,
)
from src.base.models import TimeStampedModel, TimeStampIndexedModel
from src.organization.models import Organization, TenantAwareModel
from src.student.models import Student
from src.teacher.models import Teacher


class StudentFee(TenantAwareModel):
    name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class AccountGroup(models.Model):
    code = models.PositiveIntegerField(default=0, unique=True)
    name = models.CharField(max_length=32)
    category = models.PositiveSmallIntegerField(choices=ACCOUNT_GROUP_TYPE)

    def __str__(self):
        return str(self.code) + " - " + self.name


class Account(TimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    gl_code = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    balance_type = models.SmallIntegerField(choices=((1, "Debit"), (-1, "Credit")))
    account_type = models.SmallIntegerField(choices=ACCOUNT_TYPE)
    group = models.ForeignKey(AccountGroup, on_delete=models.CASCADE)
    editable = models.BooleanField(default=True)

    class Meta:
        unique_together = (("organization", "name"),)
        indexes = [Index(fields=["organization", "name"])]

    def __str__(self):
        return self.name

    def is_invalid(self):
        return self.transactions.exists() and not self.is_active

    def balance(self, start_date=None, end_date=None):
        transactions = self.transactions.filter(journal__is_posted=True)
        trans = (
            transactions.filter(
                journal__posted_date__gte=start_date, journal__posted_date__lte=end_date
            )
            if end_date
            else transactions.filter(journal__posted_date__lte=datetime.now())
        )

        return (
            trans.aggregate(balance=Coalesce(Sum(F("debit") - F("credit")), 0))[
                "balance"
            ]
            * self.balance_type
        )


class Transaction(TimeStampIndexedModel):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions"
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    type = models.SmallIntegerField(choices=TRANSACTION_TYPE, default=1)
    amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    debit = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    journal = models.ForeignKey(
        "Journal", on_delete=models.CASCADE, related_name="transactions"
    )
    detail = models.CharField(max_length=50, blank=True)
    extra_ref = models.CharField(max_length=20, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [Index(fields=["organization", "account"]), Index(fields=["journal"])]

    def save(self, *args, **kwargs):
        if self.debit and self.credit:
            raise ValueError("Cannot insert debit and credit both")

        super().save(*args, **kwargs)


class BaseEntry(TimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    posted_date = models.DateField(null=True, blank=True)
    number = models.PositiveIntegerField(default=0)

    description = models.CharField(max_length=52, null=True, blank=True)

    # below 3 fields are for future references
    approved = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_posted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        indexes = [Index(fields=["organization", "posted_date"])]


class Journal(BaseEntry):
    document_date = models.DateField(null=True, blank=True)
    reference = models.CharField(max_length=20, null=True, blank=True)
    invoice = models.OneToOneField(
        "Invoice", on_delete=models.CASCADE, null=True, blank=True
    )
    payment = models.OneToOneField(
        "Payment", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        indexes = [Index(fields=["invoice"]), Index(fields=["payment"])]

    def validate(self):
        debit = credit = 0
        for t in self.transactions.all():
            debit += t.debit
            credit += t.credit
        return False if debit != credit else True


class Invoice(BaseEntry):
    due_date = models.DateField(null=True)
    document_type = models.PositiveSmallIntegerField(choices=DOC_TYPE, default=0)

    base_amount = models.DecimalField(decimal_places=2, max_digits=11, default=0)
    discount = models.DecimalField(decimal_places=2, max_digits=11, default=0.0)
    net_amount = models.DecimalField(decimal_places=2, max_digits=11, default=0)

    student = models.ForeignKey(
        Student, on_delete=models.PROTECT, null=True, blank=True
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.PROTECT, null=True, blank=True
    )

    def __str__(self):
        return "{}-{}".format(self.get_document_type_display(), self.number)

    def calculate_net_amount(self):
        self.net_amount = self.base_amount * (1 - self.discount / Decimal(100.0))

    @property
    def due_amount(self):
        paid_amount = sum(p.net_amount for p in self.payments.all())
        return round(float(self.net_amount) - paid_amount, 2)


class Payment(BaseEntry):
    type = models.PositiveSmallIntegerField(choices=PAYMENT_TYPE, default=0)
    mode = models.PositiveSmallIntegerField(choices=PAYMENT_MODE, default=0)

    base_amount = models.DecimalField(decimal_places=2, max_digits=11)
    discount = models.DecimalField(decimal_places=2, max_digits=11, default=0.0)
    net_amount = models.DecimalField(decimal_places=2, max_digits=11, default=0)

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True, blank=True
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.PROTECT, null=True, blank=True
    )

    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="payments"
    )

    def calculate_net_amount(self):
        self.net_amount = self.base_amount * (1 - self.discount / Decimal(100.0))

    def __str__(self):
        return "{}-{}".format(self.get_type_display(), self.number)
