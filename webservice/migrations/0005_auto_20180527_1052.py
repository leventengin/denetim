# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-27 07:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0004_auto_20180526_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rfid_dosyasi',
            name='rfid_no',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='yer_updown',
            name='mac_no',
            field=models.CharField(max_length=20),
        ),
    ]
