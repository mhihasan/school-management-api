# Generated by Django 3.0.4 on 2020-05-27 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_auto_20200326_2337"),
    ]

    operations = [
        migrations.RemoveField(model_name="user", name="is_student",),
        migrations.RemoveField(model_name="user", name="username",),
        migrations.AddField(
            model_name="user",
            name="is_guardian",
            field=models.BooleanField(
                default=False,
                help_text="Designates whether the user is guardian.",
                verbose_name="guardian status",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="email address"
            ),
        ),
    ]
