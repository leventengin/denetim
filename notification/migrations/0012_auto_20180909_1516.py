# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-09 12:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0011_auto_20180902_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 9, 15, 16, 17, 169548)),
        ),
    ]