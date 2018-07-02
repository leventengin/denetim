import json
import requests
from django.contrib.auth.models import User, Group
from django.shortcuts import render, render_to_response
from webservice.models import Memnuniyet, Operasyon_Data, rfid_dosyasi, Denetim_Data, Ariza_Data
from .models import yer
import datetime


def proje_varmi_kontrol(request):
    user = request.user
    if (user.profile.opr_alan_sefi == "E"  or  user.profile.opr_proje_yon == "E" or user.profile.isletme_projeyon == "E"):
        proje = user.profile.proje
        print("proje", proje)
        if proje == None:
            print("kişiye atanmış proje yok")
            mesaj = "kişiye atanmış proje yok..."
            return False
            #return render(request, 'islem/uyari.html', {'mesaj': mesaj})
        else:
            return True

    else:
        print("buraya geldi...proje yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return False
        #return render(request, 'islem/uyari.html', {'mesaj': mesaj})




def sirket_varmi_kontrol(request):
    user = request.user
    if (user.profile.operasyon_merkezyon == "E"):
        sirket = user.profile.sirket
        print("şirket", sirket)
        if sirket == None:
            print("kişiye atanmış şirket yok")
            mesaj = "kişiye atanmış şirket yok..."
            return False
        else:
            return True

    else:
        print("buraya geldi...şirket tanımlı değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return False


def get_m_list(request):
    proje = request.user.profile.proje
    bugun = datetime.datetime.now()
    yedigun = datetime.timedelta(7,0,0)
    yedigun_once = bugun - yedigun
    memnuniyet_obj = Memnuniyet.objects.filter(proje=proje).filter(gelen_tarih__gt=yedigun_once).order_by("-id")
    m_list = []
    for x in memnuniyet_obj:
        temp = {}

        ara_tarih = x.gelen_tarih
        temp['gelen_tarih'] = ara_tarih

        mac_no = x.mac_no
        yer_obj = yer.objects.filter(mac_no=mac_no).first()
        if yer_obj:
            temp['yer'] = yer_obj.yer_adi
        else:
            temp['yer'] = mac_no

        temp['proje'] = x.proje.proje_adi

        oy = x.oy
        sebep = x.sebep
        #print("oy", oy)
        #print("sebep", sebep)

        if oy == "3":
            temp['deger'] = 0
        else:
            temp['deger'] = None

        if oy == "1":
            temp['aciklama'] = "çok mutlu"
        elif oy == "2":
            temp['aciklama'] = "mutlu"
        else:
            if sebep == "1":
                temp['aciklama'] = "sabunluk"
            if sebep == "2":
                temp['aciklama'] = "lavabo"
            if sebep == "3":
                temp['aciklama'] = "havlu"
            if sebep == "4":
                temp['aciklama'] = "koku"
            if sebep == "5":
                temp['aciklama'] = "tuvalet"
            if sebep == "6":
                temp['aciklama'] = "tuvalet kağıdı"
        m_list.append(temp)
    print("service get m list çalıştı......")
    return m_list


def get_o_list(request):
    proje = request.user.profile.proje
    bugun = datetime.datetime.now()
    yedigun = datetime.timedelta(7,0,0)
    yedigun_once = bugun - yedigun
    operasyon_obj = Operasyon_Data.objects.filter(proje=proje).filter(bas_tarih__gt=yedigun_once).order_by("-id")
    print("işte operasyon listesi...", operasyon_obj)
    o_list = []
    for x in operasyon_obj:
        temp = {}
        #bas_tarih = str(x.bas_tarih)
        #son_tarih = str(x.son_tarih)

        temp['bas_tarih'] = x.bas_tarih
        temp['son_tarih'] = x.son_tarih

        mac_no = x.mac_no
        yer_obj = yer.objects.filter(mac_no=mac_no).first()
        if yer_obj:
            temp['yer'] = yer_obj.yer_adi
        else:
            temp['yer'] = mac_no

        temp['proje'] = x.proje.proje_adi

        rfid_obj = rfid_dosyasi.objects.filter(rfid_no=x.rfid_no).first()
        if rfid_obj:
            temp['adi'] = rfid_obj.adi
            temp['soyadi'] = rfid_obj.soyadi
        else:
            temp['adi'] = ""
            temp['soyadi'] = ""

        #ara_sure = x.son_tarih - x.bas_tarih
        #temp['sure'] = str(ara_sure)
        temp['sure'] = x.son_tarih - x.bas_tarih
        print("süre....", temp['sure'])

        if x.bild_tipi == "A":
            temp['deger'] = 0
        else:
            temp['deger'] = None

        o_list.append(temp)
    return o_list


def get_d_list(request):
    proje = request.user.profile.proje
    bugun = datetime.datetime.now()
    yedigun = datetime.timedelta(7,0,0)
    yedigun_once = bugun - yedigun
    denetim_obj = Denetim_Data.objects.filter(proje=proje).filter(gelen_tarih__gt=yedigun_once).order_by("-id")
    print("işte denetim listesi...", denetim_obj)
    d_list = []
    for x in denetim_obj:
        temp = {}

        gelen_tarih = x.gelen_tarih
        temp['gelen_tarih'] = gelen_tarih

        mac_no = x.mac_no
        yer_obj = yer.objects.filter(mac_no=mac_no).first()
        if yer_obj:
            temp['yer'] = yer_obj.yer_adi
        else:
            temp['yer'] = mac_no

        #proje_no = x.proje
        #proje_obj = proje.objects.get(id=proje_no)
        #if proje_obj:
        temp['proje'] = x.proje.proje_adi
        #else:
        #    temp['proje'] = proje
        rfid_obj = rfid_dosyasi.objects.filter(rfid_no=x.rfid_no).first()
        if rfid_obj:
            temp['adi'] = rfid_obj.adi
            temp['soyadi'] = rfid_obj.soyadi
        else:
            temp['adi'] = ""
            temp['soyadi'] = ""

        sayi = int(x.kod)
        print("işte gelen kodun sayısal hali...", sayi)

        if sayi == 0:
            temp['deger'] = None
        else:
            temp['deger'] = 5

        sabun = sayi // 32
        sayi = sayi % 32
        lavabo = sayi // 16
        sayi = sayi % 16
        havlu = sayi // 8
        sayi = sayi % 8
        koku = sayi // 4
        sayi = sayi % 4
        tuvalet = sayi // 2
        kagit = sayi % 2

        aciklama = ""
        if sabun == 1:
            aciklama = aciklama + " sabun -"
        if lavabo == 1:
            aciklama = aciklama + " lavabo -"
        if havlu == 1:
            aciklama = aciklama + " havlu -"
        if koku == 1:
            aciklama = aciklama + " koku -"
        if tuvalet == 1:
            aciklama = aciklama + " tuvalet -"
        if kagit == 1:
            aciklama = aciklama + " kağıt -"

        temp['aciklama'] = aciklama

        d_list.append(temp)

    return d_list





def get_a_list(request):
    proje = request.user.profile.proje
    bugun = datetime.datetime.now()
    yedigun = datetime.timedelta(7,0,0)
    yedigun_once = bugun - yedigun
    ariza_obj = Ariza_Data.objects.filter(proje=proje).filter(gelen_tarih__gt=yedigun_once).order_by("-id")
    a_list = []
    for x in ariza_obj:
        temp = {}
        temp['gelen_tarih'] = x.gelen_tarih
        mac_no = x.mac_no
        yer_obj = yer.objects.filter(mac_no=mac_no).first()
        if yer_obj:
            temp['yer'] = yer_obj.yer_adi
        else:
            temp['yer'] = mac_no

        temp['proje'] = x.proje.proje_adi
        rfid_obj = rfid_dosyasi.objects.filter(rfid_no=x.rfid_no).first()
        if rfid_obj:
            temp['adi'] = rfid_obj.adi
            temp['soyadi'] = rfid_obj.soyadi
        else:
            temp['adi'] = ""
            temp['soyadi'] = ""

        sebep = x.sebep
        print("sebep", sebep)

        temp['deger'] = 0

        if sebep == "1":
            temp['aciklama'] = "mekanik"
        if sebep == "2":
            temp['aciklama'] = "elektrik"
        if sebep == "3":
            temp['aciklama'] = "su"
        if sebep == "4":
            temp['aciklama'] = "ayna"
        a_list.append(temp)

    return a_list



def get_memnuniyet_list():
    print("get memnuniyet list .............")
    r = requests.get("http://127.0.0.1:7000/ws/memnuniyet_list", auth=("admin", "masanata"))
    json_data = r.json()
    print(json_data)
    return json_data

def get_operasyon_list():
    print("get operasyon list .............")
    r = requests.get("http://127.0.0.1:7000/ws/operasyon_list", auth=("admin", "masanata"))
    json_data = r.json()
    print(json_data)
    return json_data

def get_denetim_saha_list():
    print("get denetim list .............")
    r = requests.get("http://127.0.0.1:7000/ws/denetim_list", auth=("admin", "masanata"))
    json_data = r.json()
    print(json_data)
    return json_data

def get_ariza_list():
    print("get ariza list .............")
    r = requests.get("http://127.0.0.1:7000/ws/ariza_list", auth=("admin", "masanata"))
    json_data = r.json()
    print(json_data)
    return json_data

def get_rfid_list():
    print("get denetim list .............")
    r = requests.get("http://127.0.0.1:7000/ws/rfid_list",  auth=("admin", "masanata"))
    json_data = r.json()
    print(json_data)
    return json_data

def get_yerud_list():
    print("get ariza list .............")
    r = requests.get("http://127.0.0.1:7000/ws/yerud_list", auth=("admin", "masanata"))
    json_data = r.json()
    print(json_data)
    return json_data
