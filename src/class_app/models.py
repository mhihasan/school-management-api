from django.db import models

# from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from datetime import datetime

# Create your models here.


class OrganizationClass(models.Model):
    name = models.CharField(max_length=150)
    # subject = ArrayField(models.CharField(max_length=200), blank=True) # ["bangla","english","islam","science"]
    subject = models.CharField(max_length=150)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)


class Section(models.Model):
    class_id = models.ForeignKey(OrganizationClass, on_delete=models.CASCADE)
    name = models.CharField(help_text=_("Section name"), max_length=150, blank=True)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
