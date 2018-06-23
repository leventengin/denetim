import json
import requests
from django.contrib.auth.models import User, Group
from django.shortcuts import render, render_to_response
from webservice.models import Memnuniyet, Operasyon_Data, rfid_dosyasi
from .models import yer


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
    memnuniyet_obj = Memnuniyet.objects.filter(proje=proje).order_by("-id")
    m_list = []
    for x in memnuniyet_obj:
        temp = {}

        ara_tarih = x.gelen_tarih

        #parsed_date = parser.parse(ara_tarih)
        parsed_date = str(ara_tarih)
        print("işte datetime a çevrilmiş hali string den ...", parsed_date)
        temp['gelen_tarih'] = parsed_date


        mac_no = x.mac_no
        yer_obj = yer.objects.filter(mac_no=mac_no).first()
        if yer_obj:
            temp['yer'] = yer_obj.yer_adi
        else:
            temp['yer'] = mac_no

        temp['proje'] = x.proje.proje_adi

        oy = x.oy
        sebep = x.sebep
        print("oy", oy)
        print("sebep", sebep)

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
    return m_list


def get_o_list(request):
    proje = request.user.profile.proje
    operasyon_obj = Operasyon_Data.objects.filter(proje=proje).order_by("-id")
    print("işte operasyon listesi...", operasyon_obj)
    o_list = []
    for x in operasyon_obj:
        temp = {}
        bas_tarih = str(x.bas_tarih)
        son_tarih = str(x.son_tarih)

        temp['bas_tarih'] = bas_tarih
        temp['son_tarih'] = son_tarih

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

        #temp['sure'] = json.dumps(x.son_tarih-x.bas_tarih)


        if x.bild_tipi == "A":
            temp['deger'] = 0
        else:
            temp['deger'] = None

        o_list.append(temp)
    return o_list



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
