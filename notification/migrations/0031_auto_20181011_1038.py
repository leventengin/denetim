# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-11 07:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0030_auto_20181010_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 11, 10, 38, 33, 457061)),
        ),
    ]
