# Generated by Django 2.1.3 on 2018-11-11 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webservice', '0020_auto_20181025_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yer_updown',
            name='yer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='islem.yer'),
        ),
    ]