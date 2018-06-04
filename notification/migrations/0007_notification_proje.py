# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-03 19:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0063_auto_20180603_2243'),
        ('notification', '0006_auto_20180429_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='proje',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='islem.proje'),
            preserve_default=False,
        ),
    ]
