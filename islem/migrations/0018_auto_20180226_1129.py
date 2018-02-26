# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-26 08:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0017_auto_20180222_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='denetim',
            name='r_erisim',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 26, 11, 29, 4, 336619)),
        ),
        migrations.AlterField(
            model_name='denetim',
            name='rutin_planli',
            field=models.CharField(choices=[('P', 'Planlı'), ('R', 'Rutin'), ('S', 'Sıralı')], max_length=1),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 26, 11, 29, 4, 333187)),
        ),
    ]
