# Generated by Django 3.0.4 on 2020-07-10 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_auto_20200612_1341'),
        ('student', '0002_auto_20200612_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialinfo',
            name='fee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounting.StudentFee'),
        ),
    ]
