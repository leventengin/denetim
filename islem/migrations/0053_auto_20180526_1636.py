# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-26 13:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0052_auto_20180526_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 26, 16, 36, 0, 295261)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 26, 16, 36, 0, 287291)),
        ),
    ]
