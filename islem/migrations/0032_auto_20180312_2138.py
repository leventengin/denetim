# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-12 18:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0031_auto_20180312_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 12, 21, 38, 41, 756778)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='puanlama_turu',
            field=models.CharField(choices=[('A', 'Onluk'), ('B', 'Beşlik'), ('C', 'İkilik')], default='A', max_length=1),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 12, 21, 38, 41, 750726)),
        ),
    ]
