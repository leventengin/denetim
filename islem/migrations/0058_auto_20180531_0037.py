# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-30 21:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0057_auto_20180527_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 31, 0, 37, 5, 155315)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 31, 0, 37, 5, 150228)),
        ),
        migrations.AlterField(
            model_name='yer',
            name='mac_no',
            field=models.CharField(max_length=20),
        ),
    ]
