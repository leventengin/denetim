# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-17 13:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0023_auto_20180917_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 17, 16, 17, 0, 543308)),
        ),
    ]