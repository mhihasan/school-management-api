# Generated by Django 3.0.4 on 2020-06-06 10:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Organization",
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
                ("name", models.CharField(max_length=50)),
                ("address", models.TextField()),
                (
                    "phone",
                    models.CharField(
                        db_index=True,
                        max_length=20,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must be entered in the format: '+999999999'. 9 to 15 digits allowed.",
                                regex="^\\+?\\d{9,15}$",
                            )
                        ],
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("google_map_link", models.URLField(blank=True, null=True)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Counter",
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
                ("invoice", models.PositiveIntegerField(default=0)),
                ("billing", models.PositiveIntegerField(default=0)),
                ("payment", models.PositiveIntegerField(default=0)),
                ("collection", models.PositiveIntegerField(default=0)),
                ("credit_note", models.PositiveIntegerField(default=0)),
                ("debit_note", models.PositiveIntegerField(default=0)),
                ("journal", models.PositiveIntegerField(default=0)),
                (
                    "organization",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="organization.Organization",
                    ),
                ),
            ],
        ),
    ]
