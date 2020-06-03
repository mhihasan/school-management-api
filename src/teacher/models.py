from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
import datetime

# imported model
from src.class_app.models import OrganizationClass, Section


class Teacher(models.Model):
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), max_length=150, blank=False)
    designation = models.CharField(
        _("teacher's designation"), max_length=150, blank=True
    )
    joining = models.DateField(_("date of joining"), blank=False)


class SalaryInfo(models.Model):
    tid = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    temp_salary = models.PositiveIntegerField(_("probational period salary"), default=0)
    temp_joining_date = models.DateField(
        _("first joining date"), auto_now=False, auto_now_add=False
    )
    permanent_salary = models.PositiveIntegerField(_("permanent employee salary"))
    perm_joining_date = models.DateField(
        _("permanent joining date"), auto_now=False, auto_now_add=False
    )
    extra_responsibility = ArrayField(models.CharField(max_length=200), blank=True)
    increment = JSONField()
    increment_history = JSONField()


class Attendance(models.Model):
    tid = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=True)


class Leave(models.Model):
    tid = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    leave_type_name = models.CharField(help_text=_("sick, marital, others"))
    days = models.PositiveIntegerField(_("number of days leave"), blank=False)
    starting_date = models.DateField(auto_now_add=False)
    end_date = models.DateField(auto_now_add=False)
    created_at = models.DateTimeField(default=datetime.now, blank=True)


class SubjectAssigned(models.Model):
    tid = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False)
    class_id = models.ForeignKey(OrganizationClass, on_delete=models.CASCADE)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
