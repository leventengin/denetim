# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-03 07:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0026_auto_20180928_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 3, 10, 9, 26, 334358)),
        ),
    ]
