# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-14 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0017_auto_20181013_2257'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ariza_data',
            old_name='kapat',
            new_name='progress',
        ),
        migrations.AddField(
            model_name='ariza_data',
            name='rfid_kapat',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
