# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-19 08:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0010_auto_20180219_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 19, 11, 41, 8, 645955)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 19, 11, 41, 8, 641689)),
        ),
    ]
