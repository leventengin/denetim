# Generated by Django 2.1.3 on 2019-03-04 18:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0097_auto_20190303_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 4, 21, 15, 2, 782764)),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 4, 21, 15, 2, 776765)),
        ),
    ]