# Generated by Django 3.0.4 on 2020-06-06 10:57

from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import src.user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("course", "0001_initial"),
        ("user", "0001_initial"),
        ("organization", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Student",
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
                ("date_created", models.DateTimeField(blank=True, null=True)),
                ("last_updated", models.DateTimeField(blank=True, null=True)),
                (
                    "first_name",
                    models.CharField(max_length=150, verbose_name="first name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=150, verbose_name="last name"),
                ),
                (
                    "gender",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Male"), (1, "Female"), (3, "Others")], default=0
                    ),
                ),
                (
                    "roll_no",
                    models.CharField(max_length=150, verbose_name="serial or roll "),
                ),
                ("present_address", django.contrib.postgres.fields.jsonb.JSONField()),
                (
                    "permanent_address",
                    django.contrib.postgres.fields.jsonb.JSONField(default=dict),
                ),
                (
                    "additional_info",
                    django.contrib.postgres.fields.jsonb.JSONField(default=dict),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="organization.Organization",
                    ),
                ),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="course.Section",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GuardianInfo",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "relationship",
                    models.CharField(
                        max_length=50, verbose_name="relation with student"
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=20,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must be entered in the format: '+999999999'. 9 to 15 digits allowed.",
                                regex="^\\+?\\d{9,15}$",
                            )
                        ],
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="guardians",
                        to="student.Student",
                    ),
                ),
            ],
            bases=("user.user",),
            managers=[("objects", src.user.models.UserManager()),],
        ),
        migrations.AddIndex(
            model_name="student",
            index=models.Index(
                fields=["section"], name="student_stu_section_f96499_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="guardianinfo",
            index=models.Index(
                fields=["student"], name="student_gua_student_c79ca7_idx"
            ),
        ),
    ]
