# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-28 07:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0083_auto_20180928_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 28, 10, 15, 10, 193042)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 28, 10, 15, 10, 187357)),
        ),
    ]
