# Generated by Django 2.2.10 on 2020-10-19 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homebudget_app', '0005_auto_20201018_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='month',
            name='month_beginning_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='month',
            name='month_end_date',
            field=models.DateField(),
        ),
    ]
