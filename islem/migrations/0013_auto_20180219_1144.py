# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-19 08:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0012_auto_20180219_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 19, 11, 44, 53, 115692)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 19, 11, 44, 53, 111938)),
        ),
    ]