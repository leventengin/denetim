# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-19 15:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0013_auto_20180219_1144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sonuc_detay',
            old_name='sayi',
            new_name='puanlama_turu',
        ),
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 19, 18, 14, 54, 191096)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 19, 18, 14, 54, 187204)),
        ),
    ]
