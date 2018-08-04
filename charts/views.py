from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from webservice.models import Memnuniyet
from islem.models import Profile, proje
from rest_framework.views import APIView
from rest_framework.response import Response
from operator import itemgetter


User = get_user_model()

class HomeView(View):
    def get(self, request, *args, **kwargs):
        print("AMA İŞLEM BURADA....................................!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return render(request, 'islem/charts.html', {"customers": 10})

def secilen_bolumu_kaydet(request):
    print("seçilen bölümü kaydet .  jquery içinden.....")
    response_data ={}
    if request.method == 'GET':
        selected = request.GET.get('selected', None)
        print("selected...:", selected )
        selected_obj = sonuc_bolum.objects.get(id=selected)
        print("selected obj", selected_obj)
        selected_bol = selected_obj.bolum.id
        print("selected_bol", selected_bol)
        if selected_bol != None:
            request.session['secili_bolum'] = selected_bol
            request.session.modified = True
            print("secili bölüm burada...:", request.session['secili_bolum'])
        else:
            print("selected none  .....  neler oluyor !!!!!")
    return HttpResponse(response_data, content_type='application/json')





def get_data(request, *args, **kwargs):

    js_proje = request.GET.get('js_proje', None)
    print("js_proje...:", js_proje )
    js_ilk_tarih = request.GET.get('js_ilk_tarih', None)
    print("js ilk tarih", js_ilk_tarih)
    js_son_tarih = request.GET.get('js_son_tarih', None)
    print("js son tarih", js_son_tarih)

    kullanici_id = request.user.id
    if js_proje == None:
        profile_obj = Profile.objects.get(id=kullanici_id)
        js_proje = profile_obj.proje.id
    p_obj = proje.objects.get(id=js_proje)
    proje_adi = str(p_obj.proje_adi)
    m_obj = Memnuniyet.objects.filter(proje=js_proje).filter(gelen_tarih__gte=js_ilk_tarih).filter(gelen_tarih__lte=js_son_tarih)

    sayısı = m_obj.count()
    print("sayısı.................:", sayısı)
    m_obj_c1 = m_obj.filter(oy="1").count()
    m_obj_c2 = m_obj.filter(oy="2").count()
    m_obj_c3 = m_obj.filter(oy="3").count()
    m_obj_toplam = m_obj_c1 + m_obj_c2 + m_obj_c3
    if m_obj_toplam != 0:
        m_yuzde_1 = round(m_obj_c1/m_obj_toplam*100, 0)
        m_yuzde_2 = round(m_obj_c2/m_obj_toplam*100, 0)
        m_yuzde_3 = round(m_obj_c3/m_obj_toplam*100, 0)
    else:
        m_yuzde_1 = m_yuzde_2 = m_yuzde_3 = 0

    labels_1 = ["Çok Memnun", "Memnun", "Memnun Değil"]
    def_items_1 = [m_obj_c1, m_obj_c2, m_obj_c3]
    print(labels_1)
    print(def_items_1)
    m_obj_oy3 = m_obj.filter(oy="3")
    m_seb1 = m_obj.filter(sebep="1").count()
    m_seb2 = m_obj.filter(sebep="2").count()
    m_seb3 = m_obj.filter(sebep="3").count()
    m_seb4 = m_obj.filter(sebep="4").count()
    m_seb5 = m_obj.filter(sebep="5").count()
    m_seb6 = m_obj.filter(sebep="6").count()
    m_seb_toplam = m_seb1 + m_seb2 + m_seb3 + m_seb4 + m_seb5 + m_seb6
    if m_seb_toplam != 0:
        s_yuzde_1 = round(m_seb1/m_seb_toplam*100, 0)
        s_yuzde_2 = round(m_seb2/m_seb_toplam*100, 0)
        s_yuzde_3 = round(m_seb3/m_seb_toplam*100, 0)
        s_yuzde_4 = round(m_seb4/m_seb_toplam*100, 0)
        s_yuzde_5 = round(m_seb5/m_seb_toplam*100, 0)
        s_yuzde_6 = round(m_seb6/m_seb_toplam*100, 0)
    else:
        s_yuzde_1 = s_yuzde_2 = s_yuzde_3 = s_yuzde_4 = s_yuzde_5 = s_yuzde_6 = 0

    labels_2 = ["Sabunluk", "Lavabo", "Havlu", "Koku", "Tuvalet", "T.Kağıdı"]
    def_items_2 = [m_seb1, m_seb2, m_seb3, m_seb4, m_seb5, m_seb6]
    print(labels_2)
    print(def_items_2)
    data = {
            "labels_1": labels_1,
            "default_1": def_items_1,
            "labels_2": labels_2,
            "default_2": def_items_2,
            "seb_toplam": m_seb_toplam,
            "seb_1": m_seb1,
            "seb_2": m_seb2,
            "seb_3": m_seb3,
            "seb_4": m_seb4,
            "seb_5": m_seb5,
            "seb_6": m_seb6,
            "mem_toplam": m_obj_toplam,
            "mem_1": m_obj_c1,
            "mem_2": m_obj_c2,
            "mem_3": m_obj_c3,
            "proje": proje_adi,
            "m_yuzde_1": m_yuzde_1,
            "m_yuzde_2": m_yuzde_2,
            "m_yuzde_3": m_yuzde_3,
            "s_yuzde_1": s_yuzde_1,
            "s_yuzde_2": s_yuzde_2,
            "s_yuzde_3": s_yuzde_3,
            "s_yuzde_4": s_yuzde_4,
            "s_yuzde_5": s_yuzde_5,
            "s_yuzde_6": s_yuzde_6,
    }
    return JsonResponse(data) # http response



def get_data_krs(request, *args, **kwargs):

    js_ilk_tarih = request.GET.get('js_ilk_tarih', None)
    print("js ilk tarih", js_ilk_tarih)
    js_son_tarih = request.GET.get('js_son_tarih', None)
    print("js son tarih", js_son_tarih)
    kullanici_id = request.user.id
    k_obj = Profile.objects.get(id=kullanici_id)
    k_sirket = k_obj.sirket
    proje_obj = proje.objects.filter(sirket=k_sirket)
    proje_count = proje_obj.count()
    p_list = []
    data_list = []
    label_list = []
    sayi = 0
    genel_toplam = 0
    memnuniyet_toplam = 0
    genel_ortalama = 0
    for i in proje_obj:
        data_row = {}
        proje_adi = str(i.proje_adi)
        m_obj = Memnuniyet.objects.filter(proje=i.id).filter(gelen_tarih__gte=js_ilk_tarih).filter(gelen_tarih__lte=js_son_tarih)
        sayısı = m_obj.count()
        print("sayısı.................:", sayısı)
        m_obj_c1 = m_obj.filter(oy="1").count()
        m_obj_c2 = m_obj.filter(oy="2").count()
        m_obj_c3 = m_obj.filter(oy="3").count()
        m_obj_toplam = m_obj_c1 + m_obj_c2 + m_obj_c3
        if m_obj_toplam != 0:
            m_obj_y1 = round(m_obj_c1/m_obj_toplam*100, 0)
            m_obj_y2 = round(m_obj_c2/m_obj_toplam*100, 0)
            m_obj_y3 = round(m_obj_c3/m_obj_toplam*100, 0)
        else:
            m_obj_y1 = m_obj_y2 = m_obj_y3 = 0
        
        sayi = sayi + 1
        memnuniyet_toplam = memnuniyet_toplam + m_obj_c1
        genel_toplam = genel_toplam + m_obj_toplam
        data_row = {
                "mem_toplam": m_obj_toplam,
                "mem_1": m_obj_c1,
                "mem_2": m_obj_c2,
                "mem_3": m_obj_c3,
                "proje": proje_adi,
                "yuzde_1": m_obj_y1,
                "yuzde_2": m_obj_y2,
                "yuzde_3": m_obj_y3,
        }
        label_row = {
                "proje": proje_adi,
        }
        data_list.append(data_row)
        label_list.append(label_row)
    if sayi != 0 and genel_toplam !=0:
        ortalama = round(memnuniyet_toplam/genel_toplam*100, 0)
    else:
        ortalama = 0
    # sort data_list.....
    data_list = sorted(data_list, key=itemgetter('mem_1'))
    data = {"data_list": data_list, "label_list": label_list, "ortalama": ortalama, "sayi": sayi}
    print("data list ....", data_list)
    return JsonResponse(data) # http response



class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        #qs_count = User.objects.all().count()
        kullanici_id = request.user.id
        p_obj = Profile.objects.get(id=kullanici_id)
        proje = p_obj.proje
        m_obj = Memnuniyet.objects.filter(proje=proje)
        m_obj_c1 = m_obj.filter(oy="1").count()
        m_obj_c2 = m_obj.filter(oy="2").count()
        m_obj_c3 = m_obj.filter(oy="3").count()
        m_obj_toplam = m_obj_c1 + m_obj_c2 + m_obj_c3
        labels_1 = ["Toplam", "Çok Memnun", "Memnun", "Memnun Değil"]
        def_items_1 = [m_obj_toplam, m_obj_c1, m_obj_c2, m_obj_c3]
        print(labels_1)
        print(def_items_1)
        m_obj_oy3 = m_obj.filter(oy="3")
        m_seb1 = m_obj.filter(sebep="1").count()
        m_seb2 = m_obj.filter(sebep="2").count()
        m_seb3 = m_obj.filter(sebep="3").count()
        m_seb4 = m_obj.filter(sebep="4").count()
        m_seb5 = m_obj.filter(sebep="5").count()
        m_seb6 = m_obj.filter(sebep="6").count()
        m_seb_toplam = m_seb1 + m_seb2 + m_seb3 + m_seb4 + m_seb5 + m_seb6
        labels_1 = ["Toplam", "Sabunluk", "Lavabo", "Havlu", "Koku", "Tuvalet", "T.Kağıdı"]
        def_items_1 = [m_seb_toplam, m_seb1, m_seb2, m_seb3, m_seb4, m_seb5, m_seb6]
        print(labels_2)
        print(def_items_2)
        data = {
                "labels": labels,
                "default": def_items,
        }
        return Response(data)
