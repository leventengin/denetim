# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-17 13:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0009_sayi_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sayi_data',
            name='adet',
            field=models.IntegerField(),
        ),
    ]