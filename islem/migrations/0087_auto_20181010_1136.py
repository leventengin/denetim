# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-10 08:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0086_auto_20181009_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 10, 11, 36, 9, 356253)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 10, 11, 36, 9, 350729)),
        ),
    ]
