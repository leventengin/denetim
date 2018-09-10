# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-09 18:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0071_auto_20180909_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 9, 21, 57, 55, 220682)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sirket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='islem.sirket'),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 9, 21, 57, 55, 215081)),
        ),
    ]
