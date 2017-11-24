# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-24 08:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0009_denetim_tipi'),
    ]

    operations = [
        migrations.CreateModel(
            name='sonuc_bolum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bolum', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='islem.bolum')),
                ('denetim', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='islem.denetim')),
            ],
        ),
    ]
