# Generated by Django 4.2.3 on 2023-07-12 04:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps", "0008_auto_20230711_2004"),
    ]

    operations = [
        migrations.AlterField(
            model_name="issue",
            name="trans_date",
            field=models.DateField(
                default=datetime.datetime(2023, 7, 12, 10, 41, 59, 645466)
            ),
        ),
        migrations.AlterField(
            model_name="requisition",
            name="requisition_date",
            field=models.DateField(
                default=datetime.datetime(2023, 7, 12, 10, 41, 59, 643484)
            ),
        ),
    ]