# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-18 09:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0048_auto_20180518_1059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='yer',
            old_name='gunden_son',
            new_name='den_son',
        ),
        migrations.RemoveField(
            model_name='yer',
            name='gunden_basl',
        ),
        migrations.RemoveField(
            model_name='yer',
            name='gunden_delta',
        ),
        migrations.AddField(
            model_name='yer',
            name='den_basl',
            field=models.TimeField(default=datetime.time(10, 0)),
        ),
        migrations.AddField(
            model_name='yer',
            name='den_delta',
            field=models.TimeField(default=datetime.time(2, 0)),
        ),
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 18, 12, 29, 15, 630925)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 18, 12, 29, 15, 624114)),
        ),
    ]
