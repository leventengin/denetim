# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-27 09:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0039_auto_20180426_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 27, 12, 10, 46, 949112)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 27, 12, 10, 46, 943799)),
        ),
    ]
