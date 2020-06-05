from django.db import models
from src.class_app.models import OrganizationClass, Section
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _
from datetime import datetime

# Create your models here.


class Student(models.Model):
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    gender = models.CharField(_("gender of student"), max_length=50)
    roll_no = models.CharField(_("serial or roll "), max_length=150, blank=False)
    admitted_class = models.OneToOneField(
        OrganizationClass, on_delete=models.CASCADE
    )  # class name six, seven, eight
    admitted_section = models.OneToOneField(
        Section, on_delete=models.CASCADE
    )  # section name kodom , kathal
    address = JSONField()
    created_at = models.DateTimeField(default=datetime.now(), blank=True)


class Fees(models.Model):
    sid = models.ForeignKey(Student, on_delete=models.CASCADE)
    admitted_fees = models.PositiveIntegerField(_("at the of admitted to organization"))
    monthly_fees = models.PositiveIntegerField(_("payable for every month"), default=0)
    additional_fees = JSONField()
    payment = models.PositiveIntegerField(_("amount of payment"))
    payment_date = models.DateField(
        _("date of payment"), auto_now=False, auto_now_add=False
    )


class GuardianInfo(models.Model):
    sid = models.ForeignKey(Student, on_delete=models.CASCADE)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    relationship = models.CharField(_("relation with student"), max_length=50)
    gender = models.CharField(_("gender of guardian"), max_length=50)
    mobile = models.CharField(_("mobil no "), max_length=20)
    email = models.EmailField(_("email address"), max_length=254)
    present_address = JSONField()
    permanent_address = JSONField()
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
