# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-17 13:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0080_auto_20180917_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 17, 16, 14, 38, 757625)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 17, 16, 14, 38, 749031)),
        ),
    ]
