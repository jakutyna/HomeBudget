# Generated by Django 2.2.10 on 2020-10-18 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homebudget_app', '0004_auto_20201018_1505'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='month',
            new_name='month_category',
        ),
    ]