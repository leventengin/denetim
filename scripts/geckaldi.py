
from django.db import models
from django.db.models import Q
from rest_framework import generics, mixins
from django.views.decorators.csrf import csrf_exempt
from webservice.models import Memnuniyet, Operasyon_Data, Denetim_Data, Ariza_Data, rfid_dosyasi, yer_updown, Sayi_Data
from notification.models import Notification
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
import datetime
import requests

def run():
    opr_data_obj = Operasyon_Data.objects.all()
    sayi = opr_data_obj.count()
    print("xxxxxxxxxxxxxxxxxxxxxx  management   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print("işte runscript çalıştı ve bize veritabanındaki sayıyı verdi...+++++", sayi)
    print("xxxxxxxxxxxxxxxxxxxxxx  management   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    simdi = datetime.datetime.now()
    Notification.objects.create(kisi_id=1,
                                proje_id=2,
                                title="crontab içinden .....",
                                message="bildirim crontab içinden .........."+str(simdi))
