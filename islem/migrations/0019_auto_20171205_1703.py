# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-05 14:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0018_auto_20171204_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='denetim',
            name='devam_mi',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='denetim',
            name='tamamla_mi',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='denetim',
            name='tekrar_mi',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sonuc',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 5, 17, 3, 34, 677193)),
        ),
    ]
