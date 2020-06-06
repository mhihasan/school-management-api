from django.db import models
from django.db.models import Index

from django.utils.translation import gettext_lazy as _

from src.base.models import TimeStampedModel
from src.organization.models import TenantAwareModel
from src.student.models import Student
from src.teacher.models import Teacher


class Course(TenantAwareModel):
    name = models.CharField(max_length=32)


class Section(TimeStampedModel):
    name = models.CharField(help_text=_("Section name"), max_length=32)
    course = models.ForeignKey(
        Course, related_name="sections", on_delete=models.CASCADE
    )

    class Meta:
        indexes = [Index(fields=["course"])]


class Subject(TimeStampedModel):
    name = models.CharField(max_length=32)
    course = models.ForeignKey(
        Course, related_name="subjects", on_delete=models.CASCADE
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        indexes = [Index(fields=["course"]), Index(fields=["teacher"])]


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    date = models.DateField(auto_now_add=True)
    is_present = models.BooleanField(default=True)

    class Meta:
        indexes = [Index(fields=["student"]), Index(fields=["teacher"])]
