# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-07 14:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0008_auto_20180607_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 7, 17, 16, 51, 44429)),
        ),
    ]