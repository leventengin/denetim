# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-12 18:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0030_auto_20180304_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 12, 21, 36, 55, 812721)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='puanlama_turu',
            field=models.CharField(choices=[('A', 'Onluk'), ('B', 'Beşlik'), ('C', 'İkilik')], max_length=1),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 12, 21, 36, 55, 806849)),
        ),
    ]