# Generated by Django 2.1.3 on 2019-03-03 16:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0038_auto_20181111_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 3, 19, 1, 31, 374391)),
        ),
    ]
