# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-28 13:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0024_auto_20180227_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='sonuc_detay',
            name='yazi_varmi',
            field=models.CharField(choices=[('E', 'Evet'), ('H', 'Hayır')], default='H', max_length=1),
        ),
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 28, 16, 29, 41, 140322)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 28, 16, 29, 41, 136808)),
        ),
    ]
