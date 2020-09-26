from django.db import models
from django.db.models import Index

from src.base.utils import phone_regex

from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _

from src.organization.models import TenantAwareModel
from src.user.models import User


def upload_path_student(instance, filename):
    return "/".join(["student", filename])


class Student(TenantAwareModel):
    GENDER = ((0, "Male"), (1, "Female"), (3, "Others"))
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    gender = models.PositiveSmallIntegerField(choices=GENDER, default=0)
    roll_no = models.CharField(_("serial or roll "), max_length=150)
    section = models.ForeignKey("course.Section", on_delete=models.DO_NOTHING)
    present_address = JSONField()
    permanent_address = JSONField(default=dict)
    additional_info = JSONField(default=dict)
    photo = models.ImageField(blank=True, null=True, upload_to=upload_path_student)
    fees = models.ManyToManyField(
        "accounting.StudentFee", through="student.FinancialInfo"
    )

    class Meta:
        indexes = [Index(fields=["section"])]


class FinancialInfo(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee = models.ForeignKey("accounting.StudentFee", on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        indexes = [Index(fields=["student", "fee"])]


class GuardianInfo(User):
    student = models.ForeignKey(
        Student, related_name="guardians", on_delete=models.CASCADE
    )
    relationship = models.CharField(_("relation with student"), max_length=50)
    phone = models.CharField(max_length=20, validators=[phone_regex])

    class Meta:
        indexes = [Index(fields=["student"])]
