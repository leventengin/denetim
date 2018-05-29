import json
import requests



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
