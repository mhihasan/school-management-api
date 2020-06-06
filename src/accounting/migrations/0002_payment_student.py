# Generated by Django 3.0.4 on 2020-06-06 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounting", "0001_initial"),
        ("student", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="student",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="student.Student",
            ),
        ),
    ]