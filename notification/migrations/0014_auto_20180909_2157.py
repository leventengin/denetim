# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-09 18:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0013_auto_20180909_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 9, 21, 57, 55, 287290)),
        ),
    ]
