# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-09 19:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0027_auto_20181003_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 9, 22, 34, 24, 50377)),
        ),
    ]
