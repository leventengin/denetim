# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-17 13:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0021_auto_20180917_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 17, 16, 13, 18, 260841)),
        ),
    ]
