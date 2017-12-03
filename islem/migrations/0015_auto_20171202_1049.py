# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-02 07:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0014_auto_20171202_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sonuc',
            name='foto',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to='cekimler/%Y/%m/%d/', width_field='width_field'),
        ),
        migrations.AlterField(
            model_name='sonuc',
            name='sayi',
            field=models.CharField(choices=[('A', 'Çok İyi'), ('B', 'İyi'), ('C', 'Orta'), ('D', 'Kötü')], default=None, max_length=1),
        ),
        migrations.AlterField(
            model_name='sonuc',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 2, 10, 49, 52, 226507)),
        ),
    ]
