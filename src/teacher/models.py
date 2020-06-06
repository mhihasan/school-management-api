from django.db import models
from django.db.models import Index
from django.utils.translation import gettext_lazy as _

from src.organization.models import TenantAwareModel
from src.user.models import User


class Designation(TenantAwareModel):
    title = models.CharField(max_length=255)


class Teacher(User):
    EMPLOYEE_TYPE = (
        (0, "Probation"),
        (1, "Full-Time"),
        (3, "Part-time"),
        (4, "Contractual"),
    )
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)
    employee_type = models.PositiveSmallIntegerField(choices=EMPLOYEE_TYPE, default=1)
    joining_date = models.DateField(auto_now=True)
    permanent_joining_date = models.DateField(null=True, blank=True)
    sections = models.ManyToManyField("course.Section", blank=True)

    class Meta:
        indexes = [Index(fields=["designation"])]


class SalaryInfo(models.Model):
    SALARY_TYPE = (
        (0, "Probation Period Salary"),
        (1, "Permanent Salary"),
        (2, "Festival Bonus"),
        (3, "Salary Increment"),
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    salary_type = models.PositiveSmallIntegerField(choices=SALARY_TYPE, default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        indexes = [Index(fields=["teacher"])]


class Leave(models.Model):
    LEAVE_TYPE = ((0, "Casual"), (1, "Sick"), (2, "Others"))
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    leave_type = models.PositiveSmallIntegerField(choices=LEAVE_TYPE, default=0)
    days = models.PositiveSmallIntegerField(_("number of days leave"), default=1)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        indexes = [Index(fields=["teacher"])]
