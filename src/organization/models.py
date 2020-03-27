from datetime import datetime

from django.db import models

from src.base.utils import phone_regex
from src.base.models import TimeStampedModel


class Organization(TimeStampedModel):
    name = models.CharField(max_length=50)
    address = models.TextField()
    registration_no = models.CharField(max_length=10)
    tin = models.CharField(max_length=12, verbose_name="TIN")
    vat_reg_no = models.CharField(max_length=15)
    phone = models.CharField(max_length=20, db_index=True, validators=[phone_regex])
    email = models.EmailField()
    website = models.URLField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    logo = models.ImageField(upload_to="images/organizations", null=True, blank=True)
    tax_submission_time = models.DateField(null=True, blank=True)
    trade_license_renew_time = models.DateField(null=True, blank=True)
    trade_license_copy = models.FileField(
        upload_to="scanned_copies", null=True, blank=True
    )
    tin_copy = models.FileField(upload_to="scanned_copies", null=True, blank=True)
    vat_copy = models.FileField(upload_to="scanned_copies", null=True, blank=True)

    def __str__(self):
        return self.name


class Counter(models.Model):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)

    invoice = models.PositiveIntegerField(default=0)
    billing = models.PositiveIntegerField(default=0)
    payment = models.PositiveIntegerField(default=0)
    collection = models.PositiveIntegerField(default=0)
    credit_note = models.PositiveIntegerField(default=0)
    debit_note = models.PositiveIntegerField(default=0)
    journal = models.PositiveIntegerField(default=0)

    def _get_prefix(self):
        time = datetime.now()
        return ((time.year % 100) * 100 + time.month) * 10000

    def next_invoice_number(self):
        self.invoice += 1
        return self._get_prefix() + self.invoice

    def next_billing_number(self):
        self.billing += 1
        return self._get_prefix() + self.billing

    def next_payment_number(self):
        self.payment += 1
        return self._get_prefix() + self.payment

    def next_collection_number(self):
        self.collection += 1
        return self._get_prefix() + self.collection

    def next_credit_note_number(self):
        self.credit_note += 1
        return self._get_prefix() + self.credit_note

    def next_debit_note_number(self):
        self.debit_note += 1
        return self._get_prefix() + self.debit_note

    def next_journal_number(self):
        self.journal += 1
        return self._get_prefix() + self.journal
