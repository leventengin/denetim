# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-16 15:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0020_auto_20171213_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sonuc',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 16, 18, 58, 7, 679673)),
        ),
    ]
