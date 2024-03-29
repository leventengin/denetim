# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-27 13:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0023_auto_20180227_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 27, 16, 9, 23, 958741)),
        ),
        migrations.AlterField(
            model_name='kucukresim',
            name='foto_kucuk',
            field=models.ImageField(blank=True, null=True, upload_to='xyz/kucukresim/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 27, 16, 9, 23, 955349)),
        ),
    ]
