# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-31 09:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0058_auto_20180531_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 31, 12, 20, 36, 600874)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 31, 12, 20, 36, 595801)),
        ),
    ]
