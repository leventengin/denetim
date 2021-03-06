# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-18 07:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0047_auto_20180429_2329'),
    ]

    operations = [
        migrations.CreateModel(
            name='plan_opr_gun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gun', models.CharField(choices=[('Pzt', 'Pazartesi'), ('Sal', 'Salı'), ('Çar', 'Çarşamba'), ('Per', 'Perşembe'), ('Cum', 'Cuma'), ('Cmt', 'Cumartesi'), ('Paz', 'Pazar')], max_length=3)),
                ('zaman', models.TimeField()),
            ],
        ),
        migrations.RenameModel(
            old_name='plan_gun',
            new_name='plan_den_gun',
        ),
        migrations.AddField(
            model_name='yer',
            name='gunden_basl',
            field=models.TimeField(default=datetime.time(8, 0)),
        ),
        migrations.AddField(
            model_name='yer',
            name='gunden_delta',
            field=models.TimeField(default=datetime.time(0, 30)),
        ),
        migrations.AddField(
            model_name='yer',
            name='gunden_son',
            field=models.TimeField(default=datetime.time(22, 0)),
        ),
        migrations.AddField(
            model_name='yer',
            name='opr_basl',
            field=models.TimeField(default=datetime.time(8, 0)),
        ),
        migrations.AddField(
            model_name='yer',
            name='opr_delta',
            field=models.TimeField(default=datetime.time(0, 30)),
        ),
        migrations.AddField(
            model_name='yer',
            name='opr_son',
            field=models.TimeField(default=datetime.time(22, 0)),
        ),
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 18, 10, 59, 7, 660163)),
        ),
        migrations.AlterField(
            model_name='ariza',
            name='tarih',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='denetim',
            name='yaratim_tarihi',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 18, 10, 59, 7, 654827)),
        ),
        migrations.AddField(
            model_name='plan_opr_gun',
            name='yer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='islem.yer'),
        ),
    ]
