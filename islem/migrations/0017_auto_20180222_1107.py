# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-22 08:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0016_auto_20180220_2209'),
    ]

    operations = [
        migrations.CreateModel(
            name='yazi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yazi', models.CharField(max_length=1500)),
            ],
        ),
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 22, 11, 7, 42, 169851)),
        ),
        migrations.AlterField(
            model_name='denetim',
            name='hedef_baslangic',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='denetim',
            name='hedef_bitis',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 22, 11, 7, 42, 166344)),
        ),
        migrations.AddField(
            model_name='yazi',
            name='denetim',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='islem.denetim'),
        ),
    ]
