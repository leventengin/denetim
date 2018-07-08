from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from webservice.models import Memnuniyet
from islem.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response


User = get_user_model()

class HomeView(View):
    def get(self, request, *args, **kwargs):
        print("AMA İŞLEM BURADA....................................!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return render(request, 'islem/charts.html', {"customers": 10})



def get_data(request, *args, **kwargs):
    kullanici_id = request.user.id
    p_obj = Profile.objects.get(id=kullanici_id)
    proje = p_obj.proje
    proje_adi = str(proje)
    m_obj = Memnuniyet.objects.filter(proje=proje)
    m_obj_c1 = m_obj.filter(oy="1").count()
    m_obj_c2 = m_obj.filter(oy="2").count()
    m_obj_c3 = m_obj.filter(oy="3").count()
    m_obj_toplam = m_obj_c1 + m_obj_c2 + m_obj_c3
    m_yuzde_1 = round(m_obj_c1/m_obj_toplam*100, 0)
    m_yuzde_2 = round(m_obj_c2/m_obj_toplam*100, 0)
    m_yuzde_3 = round(m_obj_c3/m_obj_toplam*100, 0)
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
    s_yuzde_1 = round(m_seb1/m_seb_toplam*100, 0)
    s_yuzde_2 = round(m_seb2/m_seb_toplam*100, 0)
    s_yuzde_3 = round(m_seb3/m_seb_toplam*100, 0)
    s_yuzde_4 = round(m_seb4/m_seb_toplam*100, 0)
    s_yuzde_5 = round(m_seb5/m_seb_toplam*100, 0)
    s_yuzde_6 = round(m_seb6/m_seb_toplam*100, 0)


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
