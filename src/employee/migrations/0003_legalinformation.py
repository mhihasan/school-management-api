# Generated by Django 3.0.4 on 2020-06-12 15:10

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import src.employee.models


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0002_auto_20200612_1341"),
    ]

    operations = [
        migrations.CreateModel(
            name="LegalInformation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nid", models.CharField(blank=True, max_length=120)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to=src.employee.models.upload_path
                    ),
                ),
                (
                    "present_address",
                    django.contrib.postgres.fields.jsonb.JSONField(blank=True),
                ),
                (
                    "permanent_address",
                    django.contrib.postgres.fields.jsonb.JSONField(blank=True),
                ),
                (
                    "education_background",
                    django.contrib.postgres.fields.jsonb.JSONField(blank=True),
                ),
                (
                    "additional_field",
                    models.TextField(verbose_name="additional information"),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="employee.Employee",
                    ),
                ),
            ],
        ),
    ]