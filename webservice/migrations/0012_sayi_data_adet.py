# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-17 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0011_remove_sayi_data_adet'),
    ]

    operations = [
        migrations.AddField(
            model_name='sayi_data',
            name='adet',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]