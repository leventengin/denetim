# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-03 19:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0062_auto_20180602_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 3, 22, 43, 17, 725335)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 3, 22, 43, 17, 720007)),
        ),
    ]