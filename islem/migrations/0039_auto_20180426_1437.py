# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-26 11:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0038_auto_20180416_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 26, 14, 37, 6, 504146)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 26, 14, 37, 6, 498622)),
        ),
    ]
