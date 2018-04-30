# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-29 15:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=120, null=True)),
                ('content', models.TextField(blank=True, max_length=120, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MacPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac_no', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Memnuniyet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac_no', models.CharField(max_length=20)),
                ('tipi', models.CharField(max_length=2)),
                ('oy', models.CharField(max_length=1)),
                ('sebep', models.CharField(max_length=2)),
                ('gelen_tarih', models.CharField(max_length=30)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
    ]
