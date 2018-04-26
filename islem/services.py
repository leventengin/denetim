import json
import requests

def get_rest_list():
    print("get rest list .............")
    r = requests.get("http://127.0.0.1:7001/api/postings", auth=("levent", "leventlevent"))
    json_data = r.json()
    print(json_data)
    return json_data

def get_mac_list():
    print("get mac list .............")
    r = requests.get("http://127.0.0.1:7001/api/postings/mac_list", auth=("levent", "leventlevent"))
    json_data = r.json()
    print(json_data)
    return json_data

def get_memnuniyet_list():
    print("get memnuniyet list .............")
    r = requests.get("http://127.0.0.1:7001/api/postings/memnuniyet_list", auth=("levent", "leventlevent"))
    json_data = r.json()
    print(json_data)
    return json_data
