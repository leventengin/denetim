# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-13 09:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0015_auto_20180909_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 13, 12, 28, 45, 159351)),
        ),
    ]