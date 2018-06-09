import json
import requests
from django.contrib.auth.models import User, Group


def proje_varmi_kontrol(user):

    if (user.profile.opr_alan_sefi == "E"  or  user.profile.opr_proje_yon == "E" or user.profile.isletme_projeyon == "E"):
        proje = user.profile.proje
        print("proje", proje)
        if proje == None:
            print("kişiye atanmış proje yok")
            mesaj = "kişiye atanmış proje yok..."
            return render(request, 'islem/uyari.html', {'mesaj': mesaj})
        else:
            return True

    else:
        print("buraya geldi...proje yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})





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
