from django.db import models
from django.db.models import Index
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField

from src.organization.models import TenantAwareModel
from src.user.models import User


def upload_path(instance, filename):
    return "/".join(["employee", filename])


class Designation(TenantAwareModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    

class Employee(User):
    EMPLOYEE_TYPE = (
        (0, "Probation"),
        (1, "Full-Time"),
        (3, "Part-time"),
        (4, "Contractual"),
    )
    BLOOD_GROUP = (
        (0, "A+"),
        (1, "A-"),
        (2, "B+"),
        (3, "B-"),
        (4, "O+"),
        (5, "O-"),
        (6, "AB+"),
        (7, "AB-"),
    )
    GENDER = ((0, "Male"), (1, "Female"), (3, "Others"))
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)
    employee_type = models.PositiveSmallIntegerField(choices=EMPLOYEE_TYPE, default=1)
    joining_date = models.DateField(auto_now=True)
    permanent_joining_date = models.DateField(null=True, blank=True)
    sections = models.ManyToManyField("course.Section", blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER, default=0)
    birth_date = models.DateField(null=True, blank=True)
    blood_group = models.PositiveIntegerField(choices=BLOOD_GROUP, default=0)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(blank=True, null=True, upload_to=upload_path)

    class Meta:
        indexes = [Index(fields=["designation"])]


class Leave(models.Model):
    LEAVE_TYPE = ((0, "Casual"), (1, "Sick"), (2, "Others"))
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.PositiveSmallIntegerField(choices=LEAVE_TYPE, default=0)
    days = models.PositiveSmallIntegerField(_("number of days leave"), default=1)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        indexes = [Index(fields=["employee"])]


class LegalInformation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    nid = models.CharField(blank=True, max_length=120)
    present_address = JSONField(default=dict)
    permanent_address = JSONField(default=dict)
    education_background = JSONField(default=dict)
    additional_info = JSONField(default=dict)
