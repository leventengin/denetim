# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-22 11:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0049_auto_20180518_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 22, 14, 50, 36, 18367)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 22, 14, 50, 36, 12865)),
        ),
    ]
