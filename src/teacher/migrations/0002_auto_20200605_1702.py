# Generated by Django 3.0.4 on 2020-06-05 17:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 6, 5, 17, 2, 28, 382981)),
        ),
    ]