# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-17 13:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0078_auto_20180917_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 17, 16, 11, 40, 583702)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 17, 16, 11, 40, 575708)),
        ),
    ]
