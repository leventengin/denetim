# Generated by Django 2.1.3 on 2018-11-05 08:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0036_auto_20181025_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 5, 11, 48, 12, 797449)),
        ),
    ]
