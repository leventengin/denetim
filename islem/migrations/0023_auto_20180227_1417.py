# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-27 11:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0022_auto_20180227_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 27, 14, 17, 11, 215379)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='xyz/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 27, 14, 17, 11, 212025)),
        ),
    ]