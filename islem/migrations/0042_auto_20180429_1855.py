# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-29 15:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0041_auto_20180429_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 29, 18, 55, 27, 418177)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 29, 18, 55, 27, 409339)),
        ),
    ]
