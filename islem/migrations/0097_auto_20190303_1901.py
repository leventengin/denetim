# Generated by Django 2.1.3 on 2019-03-03 16:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islem', '0096_auto_20181111_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acil',
            name='acik_kapandi',
            field=models.CharField(choices=[('A', 'Open'), ('K', 'Closed')], default='A', max_length=1),
        ),
        migrations.AlterField(
            model_name='acil',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 3, 19, 1, 31, 308955)),
        ),
        migrations.AlterField(
            model_name='bolum',
            name='bolum_kodu',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='denetim',
            name='rutin_planli',
            field=models.CharField(choices=[('P', 'Planned'), ('R', 'Routine'), ('S', 'Ordered'), ('C', 'Checklist'), ('D', 'Operation')], max_length=1),
        ),
        migrations.AlterField(
            model_name='denetim',
            name='yazi_varmi',
            field=models.CharField(choices=[('E', 'Yes'), ('H', 'No')], default='H', max_length=1),
        ),
        migrations.AlterField(
            model_name='detay',
            name='detay_kodu',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='detay',
            name='puanlama_turu',
            field=models.CharField(choices=[('A', 'Ten based'), ('B', 'Five based'), ('C', 'Two based')], default='A', max_length=1),
        ),
        migrations.AlterField(
            model_name='eleman',
            name='aktifcalisan',
            field=models.CharField(choices=[('E', 'Active Worker'), ('H', 'Left')], default='E', max_length=1),
        ),
        migrations.AlterField(
            model_name='plan_den_gun',
            name='gun',
            field=models.CharField(choices=[('Pzt', 'Monday'), ('Sal', 'Tuesday'), ('Çar', 'Wednesday'), ('Per', 'Thursday'), ('Cum', 'Friday'), ('Cmt', 'Saturday'), ('Paz', 'Sunday')], max_length=3),
        ),
        migrations.AlterField(
            model_name='plan_opr_gun',
            name='gun',
            field=models.CharField(choices=[('Pzt', 'Monday'), ('Sal', 'Tuesday'), ('Çar', 'Wednesday'), ('Per', 'Thursday'), ('Cum', 'Friday'), ('Cmt', 'Saturday'), ('Paz', 'Sunday')], max_length=3),
        ),
        migrations.AlterField(
            model_name='profile',
            name='aktifcalisan',
            field=models.CharField(choices=[('E', 'Active Worker'), ('H', 'Left')], default='E', max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='denetci',
            field=models.CharField(choices=[('E', 'Yes'), ('H', 'No')], default='H', max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='denetim_grup_yetkilisi',
            field=models.CharField(choices=[('E', 'Yes'), ('H', 'No')], default='H', max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='isletme_projeyon',
            field=models.CharField(choices=[('E', 'Yes'), ('H', 'No')], default='H', max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='opr_admin',
            field=models.CharField(choices=[('E', 'Yes'), ('H', 'No')], default='H', max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='opr_alan_sefi',
            field=models.CharField(choices=[('E', 'Yes'), ('H', 'No')], default='H', max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='opr_merkez_yon',
            field=models.CharField(choices=[('E', 'Yes'), ('H', 'No')], default='H', max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='opr_proje_yon',
            field=models.CharField(choices=[('E', 'Yes'), ('H', 'No')], default='H', max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='opr_teknik',
            field=models.CharField(choices=[('E', 'Yes'), ('H', 'No')], default='H', max_length=1),
        ),
        migrations.AlterField(
            model_name='sirket',
            name='turu',
            field=models.CharField(choices=[('D', 'Auditor Company'), ('P', 'Project Company')], default='P', max_length=1),
        ),
        migrations.AlterField(
            model_name='sonuc_bolum',
            name='tamam',
            field=models.CharField(choices=[('E', 'Yes'), ('H', 'No')], default='H', max_length=1),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='denetim_disi',
            field=models.CharField(choices=[('E', 'Yes'), ('H', 'No')], default='H', max_length=1),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='puanlama_turu',
            field=models.CharField(choices=[('A', 'Ten based'), ('B', 'Five based'), ('C', 'Two based')], default='A', max_length=1),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='tamam',
            field=models.CharField(choices=[('E', 'Yes'), ('H', 'No')], default='H', max_length=1),
        ),
        migrations.AlterField(
            model_name='sonuc_detay',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 3, 19, 1, 31, 303146)),
        ),
        migrations.AlterField(
            model_name='sonuc_resim',
            name='resim_kalktimi',
            field=models.CharField(choices=[('E', 'Yes'), ('H', 'No')], default='H', max_length=1),
        ),
        migrations.AlterField(
            model_name='tipi',
            name='tipi_kodu',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='zon',
            name='zon_kodu',
            field=models.CharField(max_length=25),
        ),
    ]