from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from webservice.models import Memnuniyet, Operasyon_Data, Ariza_Data, Denetim_Data, Sayi_Data, rfid_dosyasi
from islem.models import Profile, proje, plan_den_gun, plan_opr_gun, denetim
from rest_framework.views import APIView
from rest_framework.response import Response
from operator import itemgetter
import datetime

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

import operator

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
        memnuniyet_toplam = memnuniyet_toplam + m_obj_c1 + m_obj_c2
        genel_toplam = genel_toplam + m_obj_toplam
        memnun_yuzdesi = round((m_obj_y1 + m_obj_y2), 0)
        memnun_yuzdesi = int(memnun_yuzdesi)
        print("memnun yüzdesi....", memnun_yuzdesi)
        data_row = {
                "memnun_yuzdesi": memnun_yuzdesi,
                "mem_toplam": m_obj_toplam,
                "mem_1": m_obj_c1,
                "mem_2": m_obj_c2,
                "mem_3": m_obj_c3,
                "proje": proje_adi,
                "yuzde_1": m_obj_y1,
                "yuzde_2": m_obj_y2,
                "yuzde_3": m_obj_y3,
                "proje": proje_adi,
        }
        label_row = {
                "proje": proje_adi,
        }

        data_list.append(data_row)
    if sayi != 0 and genel_toplam !=0:
        ortalama = round(memnuniyet_toplam/genel_toplam*100, 0)
    else:
        ortalama = 0
    # sort data_list.....
    print("data list before sorting...", data_list)
    #data_list.sort(key=operator.itemgetter('memnun_yuzdesi'))
    data_list = sorted(data_list, key=lambda k: k['memnun_yuzdesi'], reverse=True)
    print("data list after sorting....", data_list)

    data = {"data_list": data_list, "ortalama": ortalama, "sayi": sayi}
    print("data list ....", data_list)
    return JsonResponse(data) # http response

#-----------------------------------------------------------------------------------------------


def ilk_tarih(tarih):
    print("ilk tarih içinden tarih...", tarih)
    #yil = tarih.year
    #ay = tarih.month
    #gun = tarih.day
    yil = int(tarih[:4])
    ay = int(tarih[5:-3])
    gun= int(tarih[-2:])
    print("yıl..",yil,"ay...",ay,"gun...",gun)
    yeni_tarih = datetime.datetime(yil, ay, gun, 0, 0, 0)
    print("işte günün başlangıcı...............", yeni_tarih)
    return yeni_tarih


def son_tarih(tarih):
    print("son tarih içinden tarih...", tarih)
    #yil = tarih.year
    #ay = tarih.month
    #gun = tarih.day
    yil = int(tarih[:4])
    ay = int(tarih[5:-3])
    gun= int(tarih[-2:])
    print("yıl..",yil,"ay...",ay,"gun...",gun)
    yeni_tarih = datetime.datetime(yil, ay, gun, 23, 59, 59)
    print("işte günün başlangıcı...............", yeni_tarih)
    return yeni_tarih



#------------------------------------------------------------------------------------------------


def gunluk_yer_mem(request, *args, **kwargs):
    yer = request.GET.get('yer', None)
    print("yer.............", yer)
    tarih = request.GET.get('tarih', None)
    print("tarih.............", tarih)
    kullanici_id = request.user.id
    #tarih = datetime.datetime.now()
    #tarih = datetime.datetime(2018, 7, 6, 11, 9, 0)
    ilk = ilk_tarih(tarih=tarih)
    son = son_tarih(tarih=tarih)

    m_list = []
    m_obj = Memnuniyet.objects.filter(yer=yer).filter(gelen_tarih__gt=ilk).filter(gelen_tarih__lt=son)
    print("işte m obj.....", m_obj)
    for m in m_obj:
        mx = []
        saat = m.gelen_tarih.hour
        print("saat.....", saat)
        dak = m.gelen_tarih.minute
        print("dakika....", dak)
        print("tamamı....", m.gelen_tarih)
        zam = str(saat).zfill(2)+":"+str(dak).zfill(2)
        print("zaman....", zam)
        mx.append(zam)

        if m.oy == "1":
            mx.append("çok memnun")
            mx.append("")
        elif m.oy == "2":
            mx.append("memnun")
            mx.append("")
        else:
            mx.append("memnun değil")
            if m.sebep == "1":
                mx.append("sabunluk")
            elif m.sebep == "2":
                mx.append("lavabo")
            elif m.sebep == "3":
                mx.append("havlu")
            elif m.sebep == "4":
                mx.append("koku")
            elif m.sebep == "5":
                mx.append("tuvalet")
            else:
                mx.append("t.kağıdı")
        m_list.append(mx)
    sorted_m = sorted(m_list, key=itemgetter(0))


    data = {"m_list": sorted_m,

            }
    print("data  ....", data)
    return JsonResponse(data)


#----------------------------------------------------------------------



def gunluk_yer_opr(request, *args, **kwargs):
    yer = request.GET.get('yer', None)
    print("gunluk yer opr ---  yer........", yer)
    tarih = request.GET.get('tarih', None)
    print("tarih.............", tarih)
    kullanici_id = request.user.id
    #tarih = datetime.datetime.now()
    #tarih = datetime.datetime(2018, 7, 6, 11, 9, 0)
    ilk = ilk_tarih(tarih=tarih)
    son = son_tarih(tarih=tarih)

    o_list = []
    gun_opr_list = []

    o_obj = Operasyon_Data.objects.filter(yer=yer).filter(bas_tarih__gt=ilk).filter(bas_tarih__lt=son)
    print("işte o obj.....", o_obj)
    for o in o_obj:
        ox = []
        #ox.append(o.bas_tarih)
        saat = o.bas_tarih.hour
        print("saat.....", saat)
        dak = o.bas_tarih.minute
        print("dakika....", dak)
        #print("tamamı....", m.gelen_tarih)
        zam = str(saat).zfill(2)+":"+str(dak).zfill(2)
        print("zaman....", zam)
        ox.append(zam)
        rf = o.rfid_no
        rf_obj = rfid_dosyasi.objects.filter(rfid_no=rf).first()
        if rf_obj.adi == None:
            ox.append(o.rfid_no)
            ox.append("")
        else:
            ox.append(rf_obj.adi)
            ox.append(rf_obj.soyadi)
        o_list.append(ox)
    sorted_o = sorted(o_list, key=itemgetter(0))






    gun_list = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz']
    gunu = ilk.weekday()
    print("===========================================================")
    print("günü mü....", gunu)
    print("===========================================================")
    secili_gun = gun_list[gunu]
    print("işte seçili olan gün...", secili_gun)

    gun_opr_obj = plan_opr_gun.objects.filter(yer=yer).filter(gun=secili_gun)
    print("işte gun opr obj.....", gun_opr_obj)
    for g in gun_opr_obj:
        gx = []
        saat = g.zaman.hour
        print("saat.....", saat)
        dak = g.zaman.minute
        print("dakika....", dak)
        zam = str(saat).zfill(2)+":"+str(dak).zfill(2)
        print("zaman....", zam)
        gx.append(zam)
        gun_opr_list.append(gx)




    data = {"o_list": sorted_o,
            "gun_opr_list": gun_opr_list,
            }
    print("data  ....", data)
    return JsonResponse(data)

#----------------------------------------------------------------------



def gunluk_yer_den(request, *args, **kwargs):
    yer = request.GET.get('yer', None)
    print("yer.............", yer)
    tarih = request.GET.get('tarih', None)
    print("tarih.............", tarih)
    kullanici_id = request.user.id
    #tarih = datetime.datetime.now()
    #tarih = datetime.datetime(2018, 7, 6, 11, 9, 0)
    ilk = ilk_tarih(tarih=tarih)
    son = son_tarih(tarih=tarih)

    d_list = []
    gun_den_list = []

    d_obj = Denetim_Data.objects.filter(yer=yer).filter(gelen_tarih__gt=ilk).filter(gelen_tarih__lt=son)
    print("işte d obj.....", d_obj)
    for d in d_obj:
        dx = []
        saat = d.gelen_tarih.hour
        print("saat.....", saat)
        dak = d.gelen_tarih.minute
        print("dakika....", dak)
        #print("tamamı....", m.gelen_tarih)
        zam = str(saat).zfill(2)+":"+str(dak).zfill(2)
        print("zaman....", zam)
        dx.append(zam)
        rf = d.rfid_no
        rf_obj = rfid_dosyasi.objects.filter(rfid_no=rf).first()
        if rf_obj.adi == None:
            dx.append(d.rfid_no)
            dx.append("")
        else:
            dx.append(rf_obj.adi)
            dx.append(rf_obj.soyadi)

        sayi = int(d.kod)

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
        if sayi == 0:
            aciklama = "eksik yok"

        dx.append(aciklama)
        d_list.append(dx)
    sorted_d = sorted(d_list, key=itemgetter(0))




    gun_list = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz']
    gunu = ilk.weekday()
    print("===========================================================")
    print("günü mü....", gunu)
    print("===========================================================")
    secili_gun = gun_list[gunu]
    print("işte seçili olan gün...", secili_gun)



    gun_den_obj = plan_den_gun.objects.filter(yer=yer).filter(gun=secili_gun)
    print("işte gun den obj.....", gun_den_obj)
    for z in gun_den_obj:
        zx = []
        saat = z.zaman.hour
        print("saat.....", saat)
        dak = z.zaman.minute
        print("dakika....", dak)
        zam = str(saat).zfill(2)+":"+str(dak).zfill(2)
        print("zaman....", zam)
        zx.append(zam)
        gun_den_list.append(zx)





    data = {"d_list": sorted_d,
            "gun_den_list": gun_den_list,
            }
    print("data  ....", data)
    return JsonResponse(data)


#----------------------------------------------------------------------



def gunluk_yer_arz(request, *args, **kwargs):
    yer = request.GET.get('yer', None)
    print("yer.............", yer)
    tarih = request.GET.get('tarih', None)
    print("tarih.............", tarih)
    kullanici_id = request.user.id
    #tarih = datetime.datetime.now()
    #tarih = datetime.datetime(2018, 7, 6, 11, 9, 0)
    ilk = ilk_tarih(tarih=tarih)
    son = son_tarih(tarih=tarih)

    a_list = []

    a_obj = Ariza_Data.objects.filter(yer=yer).filter(gelen_tarih__gt=ilk).filter(gelen_tarih__lt=son)
    print("işte a obj.....", a_obj)
    for a in a_obj:
        ax = []
        saat = a.gelen_tarih.hour
        print("saat.....", saat)
        dak = a.gelen_tarih.minute
        print("dakika....", dak)
        #print("tamamı....", m.gelen_tarih)
        zam = str(saat).zfill(2)+":"+str(dak).zfill(2)
        print("zaman....", zam)
        ax.append(zam)

        if a.progress == "0":
            ax.append("Arıza Kaydı")
            ax.append(a.num)
            rf = a.rfid_no
            rf_obj = rfid_dosyasi.objects.filter(rfid_no=rf).first()
        else:
            ax.append("Kayıt Kapatma")
            ax.append(a.num)
            rf = a.rfid_kapat
            rf_obj = rfid_dosyasi.objects.filter(rfid_kapat=rf).first()

        if rf_obj.adi == None:
            ax.append(a.rfid_no)
            ax.append("")
        else:
            ax.append(rf_obj.adi)
            ax.append(rf_obj.soyadi)

        sebep = a.sebep
        if sebep == "":
            ax.append("")
        if sebep == "0":
            ax.append("")
        if sebep == "1":
            ax.append("Mekanik")
        if sebep == "2":
            ax.append("Elektrik")
        if sebep == "3":
            ax.append("Su")
        if sebep == "4":
            ax.append("Ayna")

        a_list.append(ax)
    sorted_a = sorted(a_list, key=itemgetter(0))

    data = {"a_list": sorted_a,
            }
    print("data  ....", data)
    return JsonResponse(data)

#----------------------------------------------------------------------



def gunluk_yer_say(request, *args, **kwargs):
    yer = request.GET.get('yer', None)
    print("yer.............", yer)
    tarih = request.GET.get('tarih', None)
    print("tarih.............", tarih)
    kullanici_id = request.user.id
    #tarih = datetime.datetime.now()
    #tarih = datetime.datetime(2018, 7, 6, 11, 9, 0)
    ilk = ilk_tarih(tarih=tarih)
    son = son_tarih(tarih=tarih)

    s_list = []

    s_obj = Sayi_Data.objects.filter(yer=yer).filter(gelen_tarih__gt=ilk).filter(gelen_tarih__lt=son)
    print("işte s obj.....", s_obj)
    for s in s_obj:
        sx = []
        saat = s.gelen_tarih.hour
        print("saat.....", saat)
        dak = s.gelen_tarih.minute
        print("dakika....", dak)
        #print("tamamı....", m.gelen_tarih)
        zam = str(saat).zfill(2)+":"+str(dak).zfill(2)
        print("zaman....", zam)
        sx.append(zam)
        sx.append(s.adet)
        s_list.append(sx)
    sorted_s = sorted(s_list, key=itemgetter(0))


    data = { "s_list": sorted_s,
            }
    print("data  ....", data)
    return JsonResponse(data)



#---------------------------------------------------------------------------------

def spv_ort_sonuc(request, *args, **kwargs):
    print("spv_ort_sonuc")
    kullanici = request.user
    denetimler = denetim.objects.filter(yaratan=kullanici).filter(durum="C")
    puan = []
    sayi = []
    x = 1
    for d in denetimler:
        puan.append(d.ortalama_puan)
        sayi.append(x)
        x = x + 1
    print("puan ve sayı", puan, sayi)
    data = {"default": puan, "labels": sayi}
    print("data  ....", data)
    return JsonResponse(data)


#---------------------------------------------------------------------------------

def denetci_ort_sonuc(request, *args, **kwargs):
    print("spv_ort_sonuc")
    kullanici = request.user
    denetimler = denetim.objects.filter(denetci=kullanici).filter(durum="C")
    puan = []
    sayi = []
    x = 1
    for d in denetimler:
        puan.append(d.ortalama_puan)
        sayi.append(x)
        x = x + 1
    print("puan ve sayı", puan, sayi)
    data = {"default": puan, "labels": sayi}
    print("data  ....", data)
    return JsonResponse(data)

#----------------------------------------------------------------------

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
