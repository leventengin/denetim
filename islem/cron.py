import kronos
import random
from django.db import models
from django.db.models import Q
from rest_framework import generics, mixins
from django.views.decorators.csrf import csrf_exempt
from webservice.models import Memnuniyet, Operasyon_Data, Denetim_Data, Ariza_Data, rfid_dosyasi, yer_updown, Sayi_Data
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404





@kronos.register('* * * * *')
def kaldigec():
    print("selam dünyalı.....kronos   ")
    print("======================================")

    opr_data_obj = Operasyon_Data.objects.all()
    sayi = opr_data_obj.count()
    print("-----------------------   kronos  --------------------------------------------------")
    print("işte runscript çalıştı ve bize veritabanındaki sayıyı verdi...+++++", sayi)
    print("-----------------------   kronos  --------------------------------------------------")
