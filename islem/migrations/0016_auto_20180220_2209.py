# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-20 19:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0015_auto_20180220_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 20, 22, 9, 18, 888384)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='puan',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 20, 22, 9, 18, 884866)),
        ),
    ]
