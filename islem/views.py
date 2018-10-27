from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect , JsonResponse
from django.views.generic import View
from django.template.loader import get_template
from islem.utils import render_to_pdf #created in step 4
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import grup, sirket, proje, tipi, bolum, detay, acil, isaretler, zon, yer, proje_alanlari
from .models import Profile, denetim, sonuc_detay, sonuc_bolum, kucukresim, sonuc_takipci, qrdosyasi
from .models import plan_opr_gun, plan_den_gun, sonuc_resim, spv_yetkilisi, eleman
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models, transaction
from islem.forms import BolumSecForm, SonucForm, SonucResimForm, DenetimSecForm, Denetim_Rutin_Baslat_Form
from islem.forms import DenetimForm,  IkiliSecForm, ProjeSecForm, SirketSecForm, MacnoYerForm, PAForm, DuzenleDenetimSecForm
from islem.forms import IlkDenetimSecForm, KucukResimForm, YaziForm, YerForm, SirketIcinProjeForm, SpvForm, DenForm
from islem.forms import AcilAcForm, AcilKapaForm, AcilDenetimSecForm, Qrcode_Form, SoruListesiForm, GunForm, GunDenForm, SaatForm, SaatDenForm
from islem.forms import Sirket_Proje_Form, RaporTarihForm, Sirket_Mem_RaporForm, BolumForm, BolumListesiForm, ZonForm, ZonListesiForm
from islem.forms import Denetim_Deneme_Form, Ikili_Deneme_Form, NebuForm, Den_Olustur_Form, SoruForm, RfidForm, RfidProjeForm
from islem.forms import ElemanForm, VatandaslikForm, YerSecForm
import collections
from django.contrib.admin.widgets import FilteredSelectMultiple
from notification.models import Notification
from webservice.models import Memnuniyet, Operasyon_Data, Denetim_Data, Ariza_Data, Sayi_Data
from webservice.models import rfid_dosyasi, yer_updown
from django.db.models import ProtectedError



#-------------------------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from weasyprint import HTML, CSS
from django.template.loader import render_to_string

from functools import reduce
from itertools import chain
from pickle import PicklingError

from django import forms
from django.core import signing
from django.db.models import Q
from django.forms.models import ModelChoiceIterator
from django.urls import reverse
from django.utils.translation import get_language
from django.conf import settings
import json
import requests
import os
#from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
import datetime
from datetime import  timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render




class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
            'today': datetime.date.today(),
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
            }
        #pdf = render_to_pdf('pdf/invoice.html', data)
        pdf = render_to_pdf('pdf/utf8.html')
        return HttpResponse(pdf, content_type='application/pdf')




class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        denetim_no = request.session.get('denetim_no')
        denetim_obj = denetim.objects.get(id=denetim_no)
        print("seçilen denetim", denetim_obj)
        denetim_adi = denetim_obj.denetim_adi
        proje = denetim_obj.proje
        denetci = denetim_obj.denetci
        tipi = denetim_obj.tipi
        yaratim_tarihi = denetim_obj.yaratim_tarihi
        yaratan = denetim_obj.yaratan
        hedef_baslangic = denetim_obj.hedef_baslangic
        hedef_bitis = denetim_obj.hedef_bitis
        gerc_baslangic = denetim_obj.gerc_baslangic
        gerc_bitis = denetim_obj.gerc_bitis
        takipci_obj = sonuc_takipci.objects.filter(denetim=denetim_no)
        i = 0
        takipciler = []
        for takipci in takipci_obj:
            takipciler.append(takipci.takipci)
            i = i + 1
        d = collections.defaultdict(list)
        bolum_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
        for bolum in bolum_obj:
            print("bolum list . bolum", bolum.bolum)
            detay_obj = sonuc_detay.objects.filter(denetim=denetim_no, bolum=bolum.bolum)
            for detay in detay_obj:
                print("detay list . detay", detay.bolum, detay.detay)
                d[detay.bolum].append(detay.detay)
        print("***********************")
        print(d)
        d.default_factory = None
        dict_bol_detay = dict(d)
        print("************************")
        print(dict_bol_detay)
        context = {'dict_bol_detay':dict_bol_detay,
                    'takipciler': takipciler,
                    'denetim_adi': denetim_adi,
                    'proje' : proje,
                    'denetci' : denetci,
                    'tipi' : tipi,
                    'yaratim_tarihi' : yaratim_tarihi,
                    'yaratan' : yaratan,
                    'hedef_baslangic' : hedef_baslangic,
                    'hedef_bitis' : hedef_bitis,
                    }
        template = get_template('pdf/is_emri.html')
        html = template.render(context).encode("UTF-8")
        page = HTML(string=html, encoding='utf-8').write_pdf()
        response = HttpResponse(page, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="denetim_isemri.pdf"'
        return response




class Generate_Rapor_PDF(View):
    def get(self, request, *args, **kwargs):


        #denetim_no = request.session.get('denetim_no')
        denetim_no = pk
        denetim_obj = denetim.objects.get(id=denetim_no)
        bolumler_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
        if not(bolumler_obj):
            messages.success(request, 'Denetime ait bölüm yok')
            return redirect('index')

        kontrol_degiskeni = True
        for bolum in bolumler_obj:
            if bolum.tamam == "H":
                kontrol_degiskeni = False

        if not(kontrol_degiskeni):
            messages.success(request, 'Tamamlanmamış bölümler var')
            return redirect('index')

        #########################################################################
        ###   RAPOR
        #########################################################################

        bolum_soru = 0
        bolum_dd = 0
        bolum_net = 0
        bolum_puan = 0
        denetim_soru = 0
        denetim_dd = 0
        denetim_net = 0
        denetim_puan = 0
        i = 0
        for bolum in bolumler_obj:
            bolum_no = bolum.bolum
            detaylar_obj = sonuc_detay.objects.filter(denetim=denetim_no).filter(bolum=bolum_no)
            print("seçilmiş olan detaylar...", detaylar_obj)
            for detay in detaylar_obj:
                bolum_soru = bolum_soru + 1
                denetim_soru = denetim_soru + 1
                if detay.denetim_disi == "E":
                    bolum_dd = bolum_dd + 1
                    denetim_dd = denetim_dd + 1
                else:
                    bolum_net = bolum_net + 1
                    bolum_puan = bolum_puan + detay.puan
                    denetim_net = denetim_net +1
                    denetim_puan = denetim_puan + detay.puan
            bolum.soru_adedi = bolum_soru
            bolum.dd_adedi = bolum_dd
            bolum.net_adet = bolum_net
            bolum.toplam_puan = bolum_puan
            ortalama_puan = bolum_puan / bolum_net
            ortalama_puan = ortalama_puan * 10
            print("ortalama puan ...", ortalama_puan)
            bolum.ortalama_puan = ortalama_puan
            bolum.save()
            print("bölüm soru...", bolum_soru, "bölüm dd", bolum_dd, "bolum net", bolum_net, "bolum puan ", bolum_puan)
            bolum_soru = 0
            bolum_dd = 0
            bolum_net = 0
            bolum_puan = 0
        denetim_obj.soru_adedi = denetim_soru
        denetim_obj.dd_adedi = denetim_dd
        denetim_obj.net_adet = denetim_net
        denetim_obj.toplam_puan = denetim_puan
        ortalama_puan = denetim_puan / denetim_net
        ortalama_puan = ortalama_puan * 10
        print("ortalama puan ...", ortalama_puan)
        denetim_obj.ortalama_puan = ortalama_puan
        denetim_obj.save()
        print("denetim soru...", denetim_soru, "denetim dd", denetim_dd, "denetim net", denetim_net, "denetim puan ", denetim_puan)



        denetim_adi = denetim_obj.denetim_adi
        proje = denetim_obj.proje
        rutin_planli = denetim_obj.rutin_planli
        denetci = denetim_obj.denetci
        tipi = denetim_obj.tipi
        yaratim_tarihi = denetim_obj.yaratim_tarihi
        yaratan = denetim_obj.yaratan
        hedef_baslangic = denetim_obj.hedef_baslangic
        hedef_bitis = denetim_obj.hedef_bitis
        gerc_baslangic = denetim_obj.gerc_baslangic
        gerc_bitis = denetim_obj.gerc_bitis
        durum = denetim_obj.durum
        rutindenetci = denetim_obj.rutindenetci
        takipci_obj = sonuc_takipci.objects.filter(denetim=denetim_no)
        print("takipci objesi...", takipci_obj)
        i = 0
        takipciler = []
        for takipci in takipci_obj:
            takipciler.append(takipci.takipci)
            i = i + 1
        print("takipciler listesi..", takipciler)
        d = collections.defaultdict(list)
        bolum_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
        for bolum in bolum_obj:
            print("bolum list . bolum", bolum.bolum)
            detay_obj = sonuc_detay.objects.filter(denetim=denetim_no, bolum=bolum.bolum).order_by('detay')
            for detay in detay_obj:
                print("detay list . detay", detay.bolum, detay.detay)
                #d[detay.bolum].append(detay.detay)
                d[bolum].append(detay)
        print("***********************")
        print(d)
        d.default_factory = None
        dict_bol_detay = dict(d)
        print("************************")
        print(dict_bol_detay)
        context = {'dict_bol_detay':dict_bol_detay,
                    'takipciler': takipciler,
                    'denetim_adi': denetim_adi,
                    'proje' : proje,
                    'rutin_planli' : rutin_planli,
                    'rutindenetci' : rutindenetci,
                    'denetci' : denetci,
                    'tipi' : tipi,
                    'yaratim_tarihi' : yaratim_tarihi,
                    'yaratan' : yaratan,
                    'hedef_baslangic' : hedef_baslangic,
                    'hedef_bitis' : hedef_bitis,
                    'durum' : durum,
                    'soru_adedi' : denetim_soru,
                    'dd_adedi' :  denetim_dd,
                    'net_adet' : denetim_net,
                    'toplam_puan' : denetim_puan,
                    'ortalama_puan' : ortalama_puan,
                    'pk' : denetim_no,
                    }
        #return render(request, 'islem/teksayfa_sil_soru.html', context )
        #return render(request, 'islem/denetim_rapor_goster.html', context )


        template = get_template('pdf/denetim_rapor.html')
        html = template.render(context).encode("UTF-8")
        page = HTML(string=html, encoding='utf-8').write_pdf()
        response = HttpResponse(page, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="denetim_raporu.pdf"'
        return response







"""
        pdf = render_to_pdf('pdf/is_emri.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Denetim_Dosyası_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

"""

#-------------------------------------------------------------------------------



@login_required
def report_example(request):
    denetim_obj = denetim.objects.all().order_by('denetim_adi')
    #varModel = Model.objects.all()
    template = get_template('pdf/weasyprint.html')
    context = {}
    context = {'denetim_obj': denetim_obj, }
    html = template.render(context).encode("UTF-8")
    page = HTML(string=html, encoding='utf-8').write_pdf()
    response = HttpResponse(page, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report_example.pdf"'
    return response




#------------------------------------------------------------------------------

def eposta_gonder(request):
    subject = 'konusu bu'
    from_email = settings.EMAIL_HOST_USER
    to_email = ['lvengin@yahoo.com', 'lvengin@gmail.com']
    email_message = ' ilk deneme bu .....'
    send_mail(subject,
              email_message,
              from_email,
              to_email,
              fail_silently=False)
    return redirect('index')

#---------------------------------------------------------------------------------
# detayların puanlanması ve foto yüklenmesi .....



def upload_file(request):
    if request.method == 'POST':
        form = SonucForm(request.POST, request.FILES)
        if form.is_valid():
            instance = sonuc_detay(foto=request.FILES['file'])
            instance.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = SonucForm()
    return render(request, 'upload.html', {'form': form})



#--------------------------------------------------------------------------------

@login_required
def index(request):
    kisi = request.user
    print("kisi", kisi)
    kullanici = Profile.objects.get(user=kisi)
    print("kullanıcı", kullanici)
    sirket = kullanici.sirket
    print("şirketi....", sirket)
    if not sirket:
        if kisi.is_superuser:
            pass
        else:
            mesaj = "kişiye tanımlı şirket yok "
            return render(request, 'islem/uyari.html', {'mesaj': mesaj})

    if kullanici.opr_merkez_yon == "E":
        print(" merkez yöneticisi   evet....")

        projeler = proje.objects.filter(sirket=sirket)
        if not projeler:
            mesaj = "şirkete tanımlı proje yok "
            return render(request, 'islem/uyari.html', {'mesaj': mesaj})

        # projeler sayılacak ilk 3 proje seçilecek.....
        # ve bu seçime göre sıraya dizilecek...
        # 3 ve ikiyse yine sıraya dizilecek...
        #

        proje_sayisi = projeler.count()
        oran_mem_list = []
        for p in projeler:
            mem_obj = Memnuniyet.objects.filter(proje=p)
            if mem_obj:
                a_list = []
                oran_mem = oran_memnuniyet(request, deger=p.id)
                a_list.append(oran_mem)
                a_list.append(p.id)
                oran_mem_list.append(a_list)

        print("işte proje sayısı...", proje_sayisi)
        print("işte ortalama değer listesi...", oran_mem_list)

        oran_mem_list.sort(reverse=True)
        print("oran mem list...  sorttan sonra...", oran_mem_list)

        mem_veri_list = ana_menu_mky_hazirla(request, oran_mem_list=oran_mem_list)
        a_list = b_list = c_list = []
        sayi = len(mem_veri_list)
        print("işte array sayısı...", sayi)
        if sayi == 3:
            a_list = mem_veri_list[0]
            b_list = mem_veri_list[1]
            c_list = mem_veri_list[2]
        elif sayi == 2:
            a_list = mem_veri_list[0]
            b_list = mem_veri_list[1]
        else:
            a_list = mem_veri_list[0]


        print(" a list", a_list)
        print(" b list", b_list)
        print(" c list", c_list)


        return render(request, 'ana_menu_mky.html',
            context={'mem_veri_list': mem_veri_list,
                      'a_list': a_list,
                       'b_list': b_list,
                        'c_list': c_list,
                         'sayi': sayi},
        )

    if kullanici.opr_proje_yon == "E"  or  kullanici.opr_alan_sefi == "E":
        print("operasyon prj yön yada alan şefi..  evet....")
        sirket = request.user.profile.sirket
        print("şirket", sirket)
        if sirket == None:
            print("kişiye atanmış şirket yok")
            mesaj = "kişiye atanmış şirket yok..."
            return render(request, 'islem/uyari.html', {'mesaj': mesaj})

        index_data = index_hazirla_proje(request)
        print("işte index data...", index_data)
        return render(request, 'ana_menu_proje.html',
            context={
            'index_data': index_data,
            },
        )

    if kullanici.isletme_projeyon == "E":
        print("operasyon prj yön yada alan şefi..  evet....")
        sirket = request.user.profile.sirket
        print("şirket", sirket)
        if sirket == None:
            print("kişiye atanmış şirket yok")
            mesaj = "kişiye atanmış şirket yok..."
            return render(request, 'islem/uyari.html', {'mesaj': mesaj})

        index_data = index_hazirla_proje(request)
        print("işte index data...", index_data)
        return render(request, 'ana_menu_proje.html',
            context={
            'index_data': index_data,
            },
        )

    if kullanici.opr_teknik == "E":
        print("operasyon teknik şefi..  evet....")
        sirket = request.user.profile.sirket
        print("şirket", sirket)
        if sirket == None:
            print("kişiye atanmış şirket yok")
            mesaj = "kişiye atanmış şirket yok..."
            return render(request, 'islem/uyari.html', {'mesaj': mesaj})

        index_data = index_hazirla_proje(request)
        print("işte index data...", index_data)
        return render(request, 'ana_menu_proje.html',
            context={
            'index_data': index_data,
            },
        )


    if kullanici.denetim_grup_yetkilisi == "E":
        print(" denetçi   evet....")
        acik_denetimler = denetim.objects.filter(durum="A")
        acik_denetimler_sirali = acik_denetimler.order_by('hedef_baslangic')
        secili_denetimler = acik_denetimler_sirali.filter(denetci=request.user).filter(rutin_planli="P")
        return render(request, 'ana_menu_dgy.html',
            context={
            'secili_denetimler': secili_denetimler,
            },
        )


    if kullanici.denetci == "E":
        print(" denetçi   evet....")
        acik_denetimler = denetim.objects.filter(durum="A")
        acik_denetimler_sirali = acik_denetimler.order_by('hedef_baslangic')
        secili_denetimler = acik_denetimler_sirali.filter(denetci=request.user).filter(rutin_planli="P")
        return render(request, 'ana_menu_denetci.html',
            context={
            'secili_denetimler': secili_denetimler,
            },
        )

    if kullanici.opr_admin == "E":
        print(" denetçi   evet....")
        acik_denetimler = denetim.objects.filter(durum="A")
        acik_denetimler_sirali = acik_denetimler.order_by('hedef_baslangic')
        secili_denetimler = acik_denetimler_sirali.filter(denetci=request.user).filter(rutin_planli="P")
        return render(request, 'ana_menu_opradmin.html',
            context={
            'secili_denetimler': secili_denetimler,
            },
        )

    if kisi.is_superuser:
        mesaj = "super user.....! "
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    else:
        mesaj = "kişiye tanımlanmış bir görev yok...! "
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})


#------------------------------------------------------------------------------

# hazırlanmış olan denetimin detayını veren ekran
# buradan pdf e dönüştürülüp kaydedilebiliyor...
# denetim hiç başlamamışsa buradan başlıyor
# eğer başlamışsa işlem devam ettirilebiliyor yada bölümler tekrar işlenebiliyor..

@login_required
def denetim_detay(request, pk=None):

    request.session['denetim_no'] = pk
    request.session.modified = True

    denetim_obj = denetim.objects.get(id=pk)
    print("seçilen denetim", denetim_obj)
    denetim_adi = denetim_obj.denetim_adi
    proje = denetim_obj.proje
    rutin_planli = denetim_obj.rutin_planli
    denetci = denetim_obj.denetci
    tipi = denetim_obj.tipi
    yaratim_tarihi = denetim_obj.yaratim_tarihi
    yaratan = denetim_obj.yaratan
    hedef_baslangic = denetim_obj.hedef_baslangic
    hedef_bitis = denetim_obj.hedef_bitis
    gerc_baslangic = denetim_obj.gerc_baslangic
    gerc_bitis = denetim_obj.gerc_bitis
    durum = denetim_obj.durum
    kisi = request.user
    if kisi == denetci:
        print("kisi..", kisi, "denetci..", denetci, "oldu ok...")
        islem_olsun = True
    else:
        print("kisi..", kisi, "denetci..", denetci, "olmadı uymadı....")
        islem_olsun = False

    takipci_obj = sonuc_takipci.objects.filter(denetim=pk)
    i = 0
    takipciler = []
    for takipci in takipci_obj:
        takipciler.append(takipci.takipci)
        i = i + 1
    print("takipci  listesi..", takipciler)
    d = collections.defaultdict(list)
    bolum_obj = sonuc_bolum.objects.filter(denetim=pk)
    for bolum in bolum_obj:
        print("bolum list . bolum", bolum.bolum)
        detay_obj = sonuc_detay.objects.filter(denetim=pk, bolum=bolum.bolum)
        for detay in detay_obj:
            print("detay list . detay", detay.bolum, detay.detay)
            d[detay.bolum].append(detay.detay)
    print("***********************")
    print(d)
    d.default_factory = None
    dict_bol_detay = dict(d)
    print("************************")
    print(dict_bol_detay)
    olustur_icinden = "E"
    context = {'dict_bol_detay':dict_bol_detay,
               'takipciler': takipciler,
               'denetim_adi': denetim_adi,
               'proje' : proje,
               'rutin_planli' : rutin_planli,
               'denetci' : denetci,
               'tipi' : tipi,
               'yaratim_tarihi' : yaratim_tarihi,
               'yaratan' : yaratan,
               'hedef_baslangic' : hedef_baslangic,
               'hedef_bitis' : hedef_bitis,
               'durum' : durum,
               'islem_olsun' : islem_olsun,
               'oluştur_icinden' : olustur_icinden,
               }
    return render(request, 'ana_menu_2.html', context )



#--------------------------------------------------------------------------------

@login_required
def denetim_baslat(request, pk=None):

    denetim_no = request.session.get('denetim_no')
    denetim_obj = denetim.objects.get(id=denetim_no)
    print("seçilen denetim", denetim_obj)

    denetim_adi = denetim_obj.denetim_adi
    proje = denetim_obj.proje
    yaratim_tarihi = denetim_obj.yaratim_tarihi

    hedef_baslangic = denetim_obj.hedef_baslangic
    hedef_bitis = denetim_obj.hedef_bitis

    context = {'denetim_adi': denetim_adi,
               'proje' : proje,
               'yaratim_tarihi' : yaratim_tarihi,
               'hedef_baslangic' : hedef_baslangic,
               'hedef_bitis' : hedef_bitis,
               }
    return render(request, 'islem/denetim_baslat_sor.html', context )



#--------------------------------------------------------------------------------

# denetimi başlatmaya karar verildiğinde durumu B yapıyor, A den B ye

@login_required
def denetim_baslat_kesin(request, pk=None):

    denetim_no = request.session.get('denetim_no')
    request.session['devam_tekrar'] = "devam"
    denetim_obj = denetim.objects.get(id=denetim_no)
    print("seçilen denetim kesin ...", denetim_obj)
    denetim_obj.durum = "B"
    denetim_obj.gerc_baslangic = datetime.datetime.now()
    denetim_obj.save()

    bolumler_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
    bolum_sayi = bolumler_obj.count()

    print("bolum sayı...:", bolum_sayi)

    if bolum_sayi == 1:
        request.session['bolum_atla_flag'] = True
    else:
        request.session['bolum_atla_flag'] = False

    return redirect('denetim_bolum_sec' )



#--------------------------------------------------------------------
# denetimine devam edilen denetimleri listeler
# buradan denetime devam edilebilir, bölümler tekrar denetlenebilir, denetim tamamlanabilir


@login_required
def devam_liste(request, pk=None):
    kisi = request.user
    print("kisi", kisi)
    kullanici = Profile.objects.get(user=kisi)
    print("kullanıcı", kullanici)

    devameden_denetimler = denetim.objects.filter(durum="B")
    devameden_denetimler_sirali = devameden_denetimler.order_by('denetim_adi')
    secili_denetimler = devameden_denetimler_sirali.filter(denetci=request.user)

    if secili_denetimler:
        for denetim_iki in secili_denetimler:
            devam_varmi = False
            tekrar_varmi = False
            tamamla_varmi = True
            sonuclar = sonuc_bolum.objects.filter(denetim=denetim_iki.id)
            for sonuc in sonuclar:
                if sonuc.tamam == "H":
                    tamamla_varmi = False
                    devam_varmi = True
                else:
                    tekrar_varmi = True
            denetim_iki.devam_mi = devam_varmi
            denetim_iki.tekrar_mi = tekrar_varmi
            denetim_iki.tamamla_mi = tamamla_varmi
            denetim_iki.save()

    return render(request, 'islem/devameden_denetimler.html',
        context={
        'secili_denetimler': secili_denetimler,
        },
    )


#--------------------------------------------------------------------
# denetimine devam edilen denetimleri listeler
# buradan denetime devam edilebilir, bölümler tekrar denetlenebilir, denetim tamamlanabilir


@login_required
def rutin_baslat(request, pk=None):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        #denetim_obj_ilk = denetim.objects.filter(durum="B") | denetim.objects.filter(durum="C")
        #denetim_obj = denetim_obj_ilk.filter(denetci=request.user)
        print("post içinden form yüklemeden önce...............")
        denetci=request.user.id
        form = Denetim_Rutin_Baslat_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            denetim_no = request.POST.get('denetim', "")
            print ("denetim seçim yapılmış...", denetim_no)
            request.session['rutin_secili_denetim'] = denetim_no
            secili_denetim = denetim.objects.get(id=denetim_no)
            print("seçili denetim...", secili_denetim)


            context = {'secili_denetim': secili_denetim}
            return render(request, 'islem/rutin_baslat_soru.html', context)
        else:
            #form = DenetimSecForm()
            return render(request, 'islem/ana_menu.html',)

    # if a GET (or any other method) we'll create a blank form
    else:
        #denetim_obj_ilk = denetim.objects.filter(durum="C") | denetim.objects.filter(durum="D")
        # buradan C kalkacak sadece D kalacak..............
        #denetim_obj = denetim_obj_ilk.filter(denetci=request.user)
        #if denetim_obj:
        #print("get çalıştı..................", denetim_obj)
        denetci=request.user.id
        print("***********************************************************")
        form = Denetim_Rutin_Baslat_Form()
        return render(request, 'islem/rutin_baslat_form.html', {'form': form,})






@transaction.atomic
@login_required
def rutin_baslat_kesin(request, pk=None):

    denetim_no = request.session.get('rutin_secili_denetim')
    print(" session içinden rutin secili denetim.......", denetim_no)

    secili_denetim = denetim.objects.get(id=denetim_no)
    dd_denetim_adi = secili_denetim.denetim_adi

    bugun = datetime.datetime.now().strftime("%Y-%m-%d")
    print("bugun...", bugun)
    dd_denetim_yeni_adi = dd_denetim_adi + "- " + str(bugun)
    print("yeni denetim adi...", dd_denetim_yeni_adi)

    # bir de  yanına sayı ver.....
    sayi = 1
    sayi_chr = "{0:0=2d}".format(sayi)
    print("sayi_chr...", sayi_chr)
    dd_denetim_sonad = dd_denetim_yeni_adi + "/" + sayi_chr
    print(" son denetim ad...", dd_denetim_sonad)
    yok_mu = True
    while yok_mu:
        arama_obj =  denetim.objects.filter(denetim_adi=dd_denetim_sonad).first()
        if arama_obj == None:
            yok_mu = False
            print("buradan çıkıyor bulamadı..")
        else:
            sayi = sayi + 1
            sayi_chr = "{0:0=2d}".format(sayi)
            print("sayi chr...", sayi_chr)
            dd_denetim_sonad = dd_denetim_yeni_adi + "/" + sayi_chr
            print(" son denetim ad...", dd_denetim_sonad)


    dd_proje =  secili_denetim.proje.id
    dd_rutin_planli = "S"
    dd_r_erisim = denetim_no
    dd_denetci = secili_denetim.denetci.id
    dd_tipi =  secili_denetim.tipi.id
    dd_hedef_baslangic =  secili_denetim.hedef_baslangic
    dd_hedef_bitis = secili_denetim.hedef_bitis
    dd_aciklama =  secili_denetim.aciklama
    dd_durum = "B"
    dd_yaratim_tarihi = bugun
    dd_yaratan = request.user.id



    print("denetim adı", dd_denetim_sonad)
    print("proje", dd_proje)
    print("r_erişim", dd_r_erisim)
    print("rutin planlı", dd_rutin_planli)
    print("denetci", dd_denetci)
    print("tipi", dd_tipi)
    print("hedef_baslangic", dd_hedef_baslangic)
    print("hedef_bitis", dd_hedef_bitis)
    print("açıklama", dd_aciklama)
    print("durum", dd_durum)
    print("yaratim tarihi", dd_yaratim_tarihi)
    print("dd_yaratan", dd_yaratan)


    kaydetme_obj = denetim(denetim_adi=dd_denetim_sonad,
                                   proje_id=dd_proje,
                                   r_erisim=dd_r_erisim,
                                   rutin_planli=dd_rutin_planli,
                                   denetci_id=dd_denetci,
                                   tipi_id=dd_tipi,
                                   hedef_baslangic="2001-01-01",
                                   hedef_bitis="2001-01-01",
                                   aciklama=dd_aciklama,
                                   yaratim_tarihi=dd_yaratim_tarihi,
                                   durum=dd_durum,
                                   yaratan=request.user
                                   )
    kaydetme_obj.save()

    yeni_obj = denetim.objects.filter(r_erisim=denetim_no).last()
    yeni_denetim_no = yeni_obj.id
    print(" yeni denetimin numarası....", yeni_denetim_no)
    print(" eski denetimin numarası....", denetim_no)


    bolumler_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
    detaylar_obj = sonuc_detay.objects.filter(denetim=denetim_no)
    takipciler_obj= sonuc_takipci.objects.filter(denetim=denetim_no)

    bolumler_list = []
    if bolumler_obj:
        for bolum in bolumler_obj:
            bolumler_list.append(bolum.bolum)

    print(bolumler_list)

    if bolumler_obj:
        for item in bolumler_list:
            print("item...", item)
            dd_denetim = yeni_denetim_no
            dd_bolum = item.id
            bolum_kaydet_obj = sonuc_bolum(denetim_id=dd_denetim,
                                            bolum_id=dd_bolum)
            bolum_kaydet_obj.save()




    bolumler_list = []
    detaylar_list = []
    puanlama_list = []
    i = 0
    if detaylar_obj:
        for detay in detaylar_obj:
            bolumler_list.append(detay.bolum)
            detaylar_list.append(detay.detay)
            puanlama_list.append(detay.puanlama_turu)


    if detaylar_obj:
        for item_bolum, item_detay, item_puanlama in zip(bolumler_list, detaylar_list, puanlama_list):
            print("item bölüm,  item detay, item_puanlama..", item_bolum, item_detay, item_puanlama)
            dd_denetim = yeni_denetim_no
            dd_bolum = item_bolum.id
            dd_detay = item_detay.id
            dd_puanlama_turu = item_puanlama
            detay_kaydet_obj = sonuc_detay(denetim_id=dd_denetim,
                                            bolum_id=dd_bolum,
                                            detay_id=dd_detay,
                                            puanlama_turu=dd_puanlama_turu)
            detay_kaydet_obj.save()




    takipciler_list = []

    if takipciler_obj:
        for takipci in takipciler_obj:
            takipciler_list.append(takipci.takipci)



    if takipciler_obj:
        for item in takipciler_list:
            print("item...", item)
            dd_denetim = yeni_denetim_no
            dd_takipci = item.id
            takipci_kaydet_obj = sonuc_takipci(denetim_id=dd_denetim,
                                               takipci_id=dd_takipci)
            takipci_kaydet_obj.save()



    request.session['devam_tekrar'] = "devam"
    request.session['denetim_no'] = yeni_denetim_no

    bolum_sayi = bolumler_obj.count()

    print("bolum sayı...:", bolum_sayi)

    if bolum_sayi == 1:
        request.session['bolum_atla_flag'] = True
    else:
        request.session['bolum_atla_flag'] = False

    return redirect('denetim_bolum_sec' )



#--------------------------------------------------------------------
# denetimine devam edilen denetimleri listeler
# buralardan merkeze acil bildirimi yapılabilir...


@login_required
def acil_devam_sec(request, pk=None):
    # if this is a POST request we need to process the form data
    denetci = request.user
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AcilAcForm(request.POST, denetci=denetci)
        print("buraya mı geldi acil aç form...")
        if form.is_valid():
            dd_denetim = request.POST.get('denetim', "")
            denetim_obj = denetim.objects.get(id=dd_denetim)
            print ("denetim ", dd_denetim)
            dd_konu = request.POST.get('konu', "")
            print ("konu", dd_konu)
            dd_aciklama = request.POST.get('aciklama', "")
            print ("aciklama", dd_aciklama)
            # veri tabanına yazıyor
            acil_obj = acil.objects.filter(denetim=dd_denetim)
            #acil_obj, created = acil.objects.get_or_create(denetim=dd_denetim)
            if not(acil_obj):
                # means you will create a new db object
                print("yeni acil kaydı..........")
                kaydetme_obj = acil(denetim_id=dd_denetim, konu=dd_konu, aciklama=dd_aciklama)
                kaydetme_obj.save()
            else:
                # just refers to the existing one
                acil_obj_2 = acil_obj.first()
                print("id  iki", acil_obj_2.id)
                print("denetim", acil_obj_2.denetim)
                kaydetme_obj = acil(id=acil_obj_2.id, denetim_id=acil_obj_2.denetim.id, konu=dd_konu, aciklama=dd_aciklama)
                kaydetme_obj.save()


            print("denetim no...", dd_denetim)
            denetim_obj = denetim.objects.get(id=dd_denetim)
            denetci = denetim_obj.denetci
            takipci_obj = sonuc_takipci.objects.filter(denetim=dd_denetim)

            ##############################################
            ###   email işlemi....................
            ##############################################


            adi = denetim_obj.yaratan.get_full_name()
            denetim_id = denetim_obj.id
            denetim_adi = denetim_obj.denetim_adi

            subject = "Denetci tarafından acil bildirim"
            to = [denetim_obj.yaratan.email]
            adi = denetim_obj.yaratan.get_full_name()
            denetim_adi = denetim_obj.denetim_adi
            konu = dd_konu
            aciklama = dd_aciklama

            from_email = settings.EMAIL_HOST_USER
            ctx = {
                'adi': adi,
                'denetim_adi': denetim_adi,
                'konu': konu,
                'aciklama': aciklama
                }
            message = get_template('islem/emt_acil_bildirim.html').render(ctx)
            msg = EmailMessage(subject, message, to=to, from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()

            takipci_obj = sonuc_takipci.objects.filter(denetim=denetim_id)

            for takipci in takipci_obj:
                adi = takipci.takipci.get_full_name()
                subject = "Denetci tarafından acil bildirim"
                to = [takipci.takipci.email]
                from_email = settings.EMAIL_HOST_USER
                ctx = {
                    'adi': adi,
                    'denetim_adi': denetim_adi,
                    'konu': konu,
                    'aciklama': aciklama
                    }
                message = get_template('islem/emt_acil_bildirim.html').render(ctx)
                msg = EmailMessage(subject, message, to=to, from_email=from_email)
                msg.content_subtype = 'html'
                msg.send()

            #connection.close()


            messages.success(request, 'Acil bildirim gönderildi')
            return redirect('index')
        else:
            return render(request, 'islem/acil_devam_sec.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = AcilAcForm(denetci=denetci)
        return render(request, 'islem/acil_devam_sec.html', {'form': form,})


#-------------------------------------------------------------------
# denetimine devam edilen denetimleri listeler
# buralardan merkeze acil bildirimi yapılabilir...


@login_required
def acil_devam_yaz(request, pk=None):
    # if this is a POST request we need to process the form data
    denetim_no = request.session.get('secili_denetim')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AcilAcForm(request.POST, denetim_no=denetim_no)
        print("buraya mı geldi acil aç form...")
        if form.is_valid():
            denetim_no = request.POST.get('denetim_no', "")
            print ("denetim no", denetim_no)
            request.session["secili_denetim"] = denetim_no
            return render(request, 'islem/acil_devam_yaz.html')
        else:
            return render(request, 'islem/acil_devam_yaz.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = AcilDenetimSecForm(denetim_no=denetim_no)
        return render(request, 'islem/acil_devam_yaz.html', {'form': form,})


#--------------------------------------------------------------------
# denetimine devam için denetimi belirle ve  bölüm seçme işlemini başlat


@login_required
def denetim_devam_islemleri(request, pk=None):
    kisi = request.user
    print("kisi", kisi)
    denetim_obj = denetim.objects.get(id=pk)
    denetim_no = denetim_obj.id
    print("denetim no ", denetim_no)
    request.session['denetim_no'] = denetim_no
    request.session['devam_tekrar'] = "devam"

    bolumler_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
    bolum_sayi = bolumler_obj.count()

    print("bolum sayı...:", bolum_sayi)

    if bolum_sayi == 1:
        request.session['bolum_atla_flag'] = True
    else:
        request.session['bolum_atla_flag'] = False

    return redirect('denetim_bolum_sec' )

#--------------------------------------------------------------------
#  tekrar edilecek bölüm seçme işlemini başlat


@login_required
def denetim_tekrar_islemleri(request, pk=None):
    kisi = request.user
    print("kisi", kisi)
    denetim_obj = denetim.objects.get(id=pk)
    denetim_no = denetim_obj.id
    print("denetim no ", denetim_no)
    request.session['denetim_no'] = denetim_no

    numarasi = denetim_obj.id
    denetim_adi = denetim_obj.denetim_adi
    context = {'denetim_adi': denetim_adi,
                'numarasi' : numarasi,
                }
    return render(request, 'islem/denetim_tekrarla_sor.html', context )





#--------------------------------------------------------------------------------

# denetim artık tamamlanıyor C - D yapılıyor....

@login_required
def denetim_tekrarla_kesin(request, pk=None):

    denetim_no = request.session.get('denetim_no')
    request.session['devam_tekrar'] = "tekrar"
    denetim_obj = denetim.objects.get(id=denetim_no)
    print("seçilen denetim kesin ...", denetim_obj)

    bolumler_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
    bolum_sayi = bolumler_obj.count()

    print("bolum sayı...:", bolum_sayi)

    if bolum_sayi == 1:
        request.session['bolum_atla_flag'] = True
    else:
        request.session['bolum_atla_flag'] = False

    return redirect('denetim_bolum_sec' )


#--------------------------------------------------------------------
#  denetimi tamamlama işlemleri önce sor sonra tamamla


@login_required
def denetim_tamamla(request, pk=None):

    tamam_bolum_tekmi = request.session.get('tamam_bolum_tekmi')
    if tamam_bolum_tekmi:
        print("tekden geldiğinin işareti olsun....")
        request.session['tamam_bolum_tekmi'] = False

    denetim_no = pk
    denetim_obj = denetim.objects.get(id=denetim_no)

    bolumler_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
    if not(bolumler_obj):
        mesaj = "tanımlı bölüm yok "
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    kontrol_degiskeni = True
    for bolum in bolumler_obj:
        if bolum.tamam == "H":
            kontrol_degiskeni = False

    if not(kontrol_degiskeni):
        mesaj = "tamamlanmamış bölümler var !"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})


    #########################################################################
    ###   RAPOR
    #########################################################################

    bolum_soru = 0
    bolum_dd = 0
    bolum_net = 0
    bolum_puan = 0
    denetim_soru = 0
    denetim_dd = 0
    denetim_net = 0
    denetim_puan = 0
    i = 0
    for bolum in bolumler_obj:
        bolum_no = bolum.bolum
        detaylar_obj = sonuc_detay.objects.filter(denetim=denetim_no).filter(bolum=bolum_no)
        print("seçilmiş olan detaylar...", detaylar_obj)
        for detay in detaylar_obj:
            bolum_soru = bolum_soru + 1
            denetim_soru = denetim_soru + 1
            if detay.denetim_disi == "E":
                bolum_dd = bolum_dd + 1
                denetim_dd = denetim_dd + 1
            else:
                bolum_net = bolum_net + 1
                bolum_puan = bolum_puan + detay.puan
                denetim_net = denetim_net +1
                denetim_puan = denetim_puan + detay.puan
        bolum.soru_adedi = bolum_soru
        bolum.dd_adedi = bolum_dd
        bolum.net_adet = bolum_net
        bolum.toplam_puan = bolum_puan
        ortalama_puan = bolum_puan / bolum_net
        ortalama_puan = ortalama_puan * 10
        print("ortalama puan ...", ortalama_puan)
        bolum.ortalama_puan = ortalama_puan
        bolum.save()
        print("bölüm soru...", bolum_soru, "bölüm dd", bolum_dd, "bolum net", bolum_net, "bolum puan ", bolum_puan)
        bolum_soru = 0
        bolum_dd = 0
        bolum_net = 0
        bolum_puan = 0
    denetim_obj.soru_adedi = denetim_soru
    denetim_obj.dd_adedi = denetim_dd
    denetim_obj.net_adet = denetim_net
    denetim_obj.toplam_puan = denetim_puan
    ortalama_puan = denetim_puan / denetim_net
    ortalama_puan = ortalama_puan * 10
    print("ortalama puan ...", ortalama_puan)
    denetim_obj.ortalama_puan = ortalama_puan
    denetim_obj.save()
    print("denetim soru...", denetim_soru, "denetim dd", denetim_dd, "denetim net", denetim_net, "denetim puan ", denetim_puan)



    denetim_adi = denetim_obj.denetim_adi
    proje = denetim_obj.proje
    rutin_planli = denetim_obj.rutin_planli
    denetci = denetim_obj.denetci.get_full_name()
    tipi = denetim_obj.tipi
    yaratan = denetim_obj.yaratan.get_full_name()
    if denetim_obj.yaratim_tarihi:
        yaratim_tarihi = denetim_obj.yaratim_tarihi.strftime("%Y-%m-%d")
    else:
        yaratim_tarihi = None
    if denetim_obj.hedef_baslangic:
        hedef_baslangic = denetim_obj.hedef_baslangic.strftime("%Y-%m-%d")
    else:
        hedef_baslangic = None
    if denetim_obj.hedef_bitis:
        hedef_bitis = denetim_obj.hedef_bitis.strftime("%Y-%m-%d")
    else:
        hedef_bitis = None
    if denetim_obj.gerc_baslangic:
        gerc_baslangic = denetim_obj.gerc_baslangic.strftime("%Y-%m-%d")
    else:
        gerc_baslangic = None
    if denetim_obj.gerc_bitis:
        gerc_bitis = denetim_obj.gerc_bitis.strftime("%Y-%m-%d")
    else:
        gerc_bitis = None
    durum = denetim_obj.durum
    rutindenetci = denetim_obj.rutindenetci
    takipci_obj = sonuc_takipci.objects.filter(denetim=denetim_no)
    print("takipci objesi...", takipci_obj)
    i = 0
    takipciler = []
    for takipci in takipci_obj:
        takipciler.append(takipci.takipci)
        i = i + 1
    print("takipciler listesi..", takipciler)
    d = collections.defaultdict(list)
    bolum_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
    for bolum in bolum_obj:
        print("bolum list . bolum", bolum.bolum)
        detay_obj = sonuc_detay.objects.filter(denetim=denetim_no, bolum=bolum.bolum).order_by('detay')
        for detay in detay_obj:
            print("detay list . detay", detay.bolum, detay.detay)
            #d[detay.bolum].append(detay.detay)
            d[bolum].append(detay)
    print("***********************")
    print(d)
    d.default_factory = None
    dict_bol_detay = dict(d)
    print("************************")
    print(dict_bol_detay)
    goster = str(round(ortalama_puan,0))
    print("göster....", goster)
    kalan = str(100 - round(ortalama_puan,0))
    print("kalan...", kalan)
    context = { 'dict_bol_detay':dict_bol_detay,
                'takipciler': takipciler,
                'denetim_adi': denetim_adi,
                'proje' : proje,
                'rutin_planli' : rutin_planli,
                'rutindenetci' : rutindenetci,
                'denetci' : denetci,
                'tipi' : tipi,
                'yaratim_tarihi' : yaratim_tarihi,
                'yaratan' : yaratan,
                'hedef_baslangic' : hedef_baslangic,
                'hedef_bitis' : hedef_bitis,
                'durum' : durum,
                'soru_adedi' : denetim_soru,
                'dd_adedi' :  denetim_dd,
                'net_adet' : denetim_net,
                'toplam_puan' : denetim_puan,
                'ortalama_puan' : ortalama_puan,
                'pk' : denetim_no,
                'goster' : goster,
                'kalan' : kalan,
                }
    #return render(request, 'islem/teksayfa_sil_soru.html', context )
    return render(request, 'islem/denetim_tamamla_sor.html', context )




#--------------------------------------------------------------------------------

# denetim artık tamamlanıyor C - D yapılıyor....

@login_required
def denetim_tamamla_kesin(request, pk=None):

    denetim_no = request.session.get('denetim_no')
    denetim_obj = denetim.objects.get(id=pk)
    print("seçilen denetim kesin ...", denetim_obj)
    denetim_obj.durum = "C"
    denetim_obj.gerc_bitis = datetime.datetime.now()
    denetim_obj.save()
    return redirect('devam_liste' )


#--------------------------------------------------------------------------------

# acil bildirim işlemleri....

@login_required
def acil_bildirim(request, pk=None):

    denetim_no = request.session.get('denetim_no')
    denetim_obj = denetim.objects.get(id=pk)
    print("seçilen denetim kesin ...", denetim_obj)
    denetim_obj.durum = "C"

    # ne olduğu belli değil...................
    #denetim_obj.save()
    return redirect('devam_liste' )


#--------------------------------------------------------------------------------

# bölümü seç ve detay işlemlerini başlat....
# seçilen bölümde detay var mı diye kontrol ediyor, aslında önceki tamam - js bunu kontrol ediyor

@login_required
def denetim_bolum_sec(request, pk=None):

    # if this is a POST request we need to process the form data
    denetim_no = request.session.get('denetim_no')
    print("denetim bölüm seç içinden denetim no ... req.ses. ile gelmiş...", denetim_no)
    bolum_atla_flag = request.session.get('bolum_atla_flag')
    print("bolum atla flag", bolum_atla_flag)

    ###################################
    # tek bölümse bölüm sorma kontrolü.....bolum atla flag....
    # tek bölümse bölüm hazırlama işlemlerini burada yapıp doğrudan gönderiyor..
    ####################################
    if bolum_atla_flag:

        bolum_obj = sonuc_bolum.objects.get(denetim=denetim_no)
        bolum = bolum_obj.bolum.id
        print ("bölüm atla içinden seçilen bolum", bolum)
        request.session["secili_bolum"] = bolum
        detaylar = sonuc_detay.objects.filter(denetim=denetim_no).filter(bolum=bolum).order_by('detay')
        print("detaylar..:", detaylar)
        if not detaylar:
            messages.success(request, 'Seçili bölümde bölüm detayı yok')
            return redirect('denetim_baslat')

        for detay in detaylar:
            print("bolum id for loop içinden", detay.bolum.id, "ve detay id", detay.detay.id)
            detay.tamam = "H"
            detay.save()
        ilk_detay_obj = detaylar.first()
        request.session['secili_detay'] = ilk_detay_obj.id
        return redirect('denetim_detay_islemleri')
        #   tek nölümse atla işlemi sonu....................


    print("denetim bölüm seç denetim no...", denetim_no)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BolumSecForm(request.POST or None)
        print("buraya mı geldi...  denetim_bolum_sec...POST")
        if form.is_valid():
            bolum = request.POST.get('bolum', "")
            print ("bolum", bolum)
            request.session["secili_bolum"] = bolum
            detaylar = sonuc_detay.objects.filter(denetim=denetim_no).filter(bolum=bolum)
            if not detaylar:
                messages.success(request, 'Seçili bölümde bölüm detayı yok')
                return redirect('denetim_baslat')
            #form = DetayForm(denetim_no=denetim_no, secili_bolum=secili_bolum)
            #form = SonucForm(puanlama_turu="")
            #print("puanlama türü boş olarak ilk adımda çalıştı ama nasıl ????????????")
            #return render(request, 'islem/denetim_detay_islemleri.html')

            for detay in detaylar:
                print("bolum id for loop içinden", detay.bolum.id, "ve detay id", detay.detay.id)
                detay.tamam = "H"
                detay.save()
            ilk_detay_obj = detaylar.first()
            request.session['secili_detay'] = ilk_detay_obj.id
            return redirect('denetim_detay_islemleri')

        else:
            print("valid değil bu form neden, ne var bunda...")
            return render(request, 'islem/denetim_bolum_sec.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        devam_tekrar = request.session.get('devam_tekrar')
        print("denetim bölüm seç içinden devam - tekrar..", devam_tekrar)
        bitir = True
        if devam_tekrar == "devam":
            kontrol_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
            for kont in kontrol_obj:
                if kont.tamam == "H":
                    bitir = False
            if bitir:
                denetim_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
                bolum_sayi = denetim_obj.count()
                if bolum_sayi == 1:
                    request.session['tamam_bolum_tekmi'] = True
                    request.session['denetim_tamamla_no'] = denetim_no
                    #return redirect('denetim_tamamla')
                    pk = denetim_no
                    print(" tek olduğunda buraya geldi tamamlaya gidecek...", denetim_no)
                    print(" denetimi tamamlıyor *****  cep telefonunda problem oluyor---nedennnnnn")

                    #return reverse('denetim_tamamla', kwargs={'pk': pk})
                else:
                    request.session['tamam_bolum_tekmi'] = False
                    messages.success(request, 'Bölüm işlemleri tamamlanmış')
                    return redirect('index')
                #return redirect('denetim_tamamla')


        form = BolumSecForm(denetim_no=denetim_no, devam_tekrar=devam_tekrar)
        return render(request, 'islem/denetim_bolum_sec.html', {'form': form,})



#--------------------------------------------------------------------------
# js içinden işlem yapılacak bölümü seçiyor....
# seçilen bölümü oturum değişkenine yazıyor

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




@login_required
@transaction.atomic
def teksayfa_yarat(request, pk=None):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        print("buraya mı geldi...  tek sayfa ...POST")
        bolum_listesi = request.session.get('js_bolumler', None)

        init_param = False
        print("bölüm listesi - tek sayfa yarat POST içinden..", bolum_listesi)
        print("init param - tek sayfa POST içinden", init_param)
        form = DenetimForm(request.POST or None, bolum_listesi=bolum_listesi)
        print(request.POST)

        if form.is_valid():
            print("neyse ki valid..bin...ext...")
            dd_denetim_adi = request.POST.get('denetim_adi', "")
            dd_proje =  request.POST.get('proje', "")
            dd_rutin_planli = request.POST.get('rutin_planli', "")
            dd_denetci = request.POST.get('denetci', "")
            dd_tipi =  request.POST.get('tipi', "")
            dd_takipciler = request.POST.getlist('takipciler', "")
            dd_hedef_baslangic =  request.POST.get('hedef_baslangic', "")
            dd_hedef_bitis = request.POST.get('hedef_bitis', "")
            dd_aciklama =  request.POST.get('aciklama', "")
            #dd_zon = request.POST.get('zon', "")
            dd_bolum = request.POST.getlist('bolum', "")
            dd_detay = request.POST.getlist('detay', "")
            if dd_rutin_planli == "R":
                dd_hedef_baslangic = "2000-01-01"
                dd_hedef_bitis = "2000-01-01"
            print("denetim adı", dd_denetim_adi)
            print("proje", dd_proje)
            print("rutin planlı", dd_rutin_planli)
            print("denetci", dd_denetci)
            print("tipi", dd_tipi)
            print("takipciler", dd_takipciler)
            print("hedef_baslangic", dd_hedef_baslangic)
            print("hedef_bitis", dd_hedef_bitis)
            print("açıklama", dd_aciklama)
            #print("zon", dd_zon)
            print("bolum", dd_bolum)
            print("detay", dd_detay)

            kaydetme_obj = denetim(denetim_adi=dd_denetim_adi,
                                   proje_id=dd_proje,
                                   rutin_planli=dd_rutin_planli,
                                   denetci_id=dd_denetci,
                                   tipi_id=dd_tipi,
                                   hedef_baslangic=dd_hedef_baslangic,
                                   hedef_bitis=dd_hedef_bitis,
                                   aciklama=dd_aciklama,
                                   yaratan=request.user
                                   )
            kaydetme_obj.save()

            denetim_obj = denetim.objects.last()
            print("son no. denetim.", denetim_obj.id, "denetim adı", denetim_obj.denetim_adi)
            denetim_no = denetim_obj.id

            i = 0
            while i < len(dd_takipciler):
                print("takipciler..", dd_takipciler[i])
                kaydetme_obj = sonuc_takipci(denetim_id=denetim_no,
                                             takipci_id=dd_takipciler[i]
                                             )
                kaydetme_obj.save()
                i = i + 1

            i = 0
            while i < len(dd_bolum):
                print("bolüm listesi..:", dd_bolum[i])
                kaydetme_obj = sonuc_bolum(denetim_id=denetim_no,
                                           bolum_id=dd_bolum[i]
                                           )
                kaydetme_obj.save()
                bolum_no = int(dd_bolum[i])
                print("son no. bolum .", bolum_no)

                j = 0
                while j < len(dd_detay):
                    detay_no = int(dd_detay[j])
                    print("işte detay no...", detay_no)
                    detayli_obj = detay.objects.get(id=detay_no)
                    olmali_bolum = detayli_obj.bolum.id
                    olmali_p_turu = detayli_obj.puanlama_turu
                    print("bölüm no", bolum_no, "olmalı bölüm :", olmali_bolum)
                    if bolum_no == olmali_bolum:
                        kaydet_obj = sonuc_detay(denetim_id=denetim_no,
                                                    bolum_id=bolum_no,
                                                    detay_id=detay_no,
                                                    puanlama_turu=olmali_p_turu
                                                    )
                        kaydet_obj.save()
                    j = j + 1

                i = i + 1



            #--------------------------------------------------------------
            # EMAIL işlemleri-----------------------------------------------
            #---------------------------------------------------------------

            #connection = mail.get_connection()
            #connection.open()

            adi = denetim_obj.denetci.get_full_name()
            denetim_id = denetim_obj.id
            denetim_adi = denetim_obj.denetim_adi
            baslangic = denetim_obj.hedef_baslangic
            bitis = denetim_obj.hedef_bitis

            subject = "Denetci olarak atandınız"
            to = [denetim_obj.denetci.email]
            from_email = settings.EMAIL_HOST_USER
            ctx = {
                'adi': adi,
                'denetim_adi': denetim_adi,
                'baslangic': baslangic,
                'bitis': bitis
                }
            message = get_template('islem/emt_denetci_oldun.html').render(ctx)
            msg = EmailMessage(subject, message, to=to, from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()

            takipci_obj = sonuc_takipci.objects.filter(denetim=denetim_id)

            for takipci in takipci_obj:
                adi = takipci.takipci.get_full_name()
                subject = "Takipçi olarak atandınız"
                to = [takipci.takipci.email]
                from_email = settings.EMAIL_HOST_USER
                ctx = {
                    'adi': adi,
                    'denetim_adi': denetim_adi,
                    'baslangic': baslangic,
                    'bitis': bitis
                    }
                message = get_template('islem/emt_takipci_oldun.html').render(ctx)
                msg = EmailMessage(subject, message, to=to, from_email=from_email)
                msg.content_subtype = 'html'
                msg.send()



            #connection.close()

            # EMAIL sonu...................................................



            #form = DenetimForm(bolum_listesi=[], init_param=True)
            #context = { 'form': form,}
            request.session['js_bolumler'] = None
            request.session['js_denetim_adi'] = None
            request.session['js_proje'] = None
            request.session['js_rutin_planli'] = None
            request.session['js_denetci'] = None
            request.session['js_tipi'] = None
            request.session['js_takipciler'] = None
            request.session['js_hedef_baslangic'] = None
            request.session['js_hedef_bitis'] = None
            request.session['js_aciklama'] = None

            messages.success(request, 'denetim başarıyla kaydedildi')
            #return render(request, 'islem/tek_sayfa.html', context,)
            return redirect('index')
        else:
            messages.success(request, ' form hatası - tekrar deneyin')
            return redirect('teksayfa_yarat')
            #return render(request, 'islem/denetim_bolum_sec.html', {'form': form,})

    # if a GET (or any other method) we'll create a blank form
    else:
        js_denetim_adi = request.session.get('js_denetim_adi', None)
        js_proje = request.session.get('js_proje', None)
        js_denetci = request.session.get('js_denetci', None)
        js_rutin_planli = request.session.get('js_rutin_planli', None)
        js_tipi = request.session.get('js_tipi', None)
        js_takipciler = request.session.get('js_takipciler', None)
        js_hedef_baslangic = request.session.get('js_hedef_baslangic', None)
        js_hedef_bitis = request.session.get('js_hedef_bitis', None)
        js_aciklama = request.session.get('js_aciklama', None)
        #js_zonlar = request.session.get('js_zonlar', None)
        js_bolumler = request.session.get('js_bolumler', None)
        bolum_listesi = js_bolumler
        init_param = True
        form = DenetimForm(bolum_listesi=bolum_listesi)
        form.fields["denetim_adi"].initial = js_denetim_adi
        form.fields["proje"].initial = js_proje
        form.fields["rp_hidden"].initial = js_rutin_planli
        print("işte js_rutin planlı....", js_rutin_planli)
        """
        if js_rutin_planli == None:
            form.fields["rutin_planli"].choices.append("P")
        else:
            form.fields["rutin_planli"].choices.append(js_rutin_planli)
        """
        form.fields["denetci"].initial = js_denetci
        form.fields["tipi"].initial = js_tipi
        form.fields["takipciler"].initial = js_takipciler
        form.fields["hedef_baslangic"].initial = js_hedef_baslangic
        form.fields["hedef_bitis"].initial = js_hedef_bitis
        form.fields["aciklama"].initial = js_aciklama
        #form.fields["zonlar"].initial = js_zonlar
        form.fields["bolum"].initial = js_bolumler
        print("buraya kadar geliyormu.............", js_tipi)
        context = { 'form': form, }
        return render(request, 'islem/tek_sayfa.html', context,)



#--------------------------------------------------------------------


def detaylarsec_bolum_js(request, pk=None):
    print("selam buraya geldik...detaylarseç bölüm js")
    print("User.id.....:", request.user.id)
    kullanan = request.user.id
    response_data ={}
    if request.method == 'GET':
        js_bolumler = request.GET.getlist('js_bolumler')
        js_denetim_adi = request.GET.get('js_denetim_adi')
        js_proje = request.GET.get('js_proje')
        js_rutin_planli = request.GET.get('js_rutin_planli')
        print("js rutin planlı detayları seçerken okunan değer...js aldığında", js_rutin_planli)
        js_denetci = request.GET.get('js_denetci')
        js_tipi = request.GET.get('js_tipi')
        js_takipciler = request.GET.getlist('js_takipciler')
        js_hedef_baslangic = request.GET.get('js_hedef_baslangic')
        js_hedef_bitis = request.GET.get('js_hedef_bitis')
        js_aciklama = request.GET.get('js_aciklama')
        #js_zonlar = request.GET.get('js_zonlar')
        request.session['js_bolumler'] = js_bolumler
        request.session['js_denetim_adi'] = js_denetim_adi
        request.session['js_proje'] = js_proje
        request.session['js_rutin_planli'] = js_rutin_planli
        request.session['js_denetci'] = js_denetci
        request.session['js_tipi'] = js_tipi
        request.session['js_takipciler'] = js_takipciler
        request.session['js_hedef_baslangic'] = js_hedef_baslangic
        request.session['js_hedef_bitis'] = js_hedef_bitis
        request.session['js_aciklama'] = js_aciklama
        #request.session['js_zonlar'] = js_zonlar
    print ("son nokta denetim bölüm js.....", response_data)
    return HttpResponse(response_data, content_type='application/json')



#--------------------------------------------------------------------


def tipisec_bolum_js(request, pk=None):
    print("selam buraya geldik...tipiseç bölüm js")
    print("User.id.....:", request.user.id)
    kullanan = request.user.id
    response_data ={}
    if request.method == 'GET':
        js_bolumler = request.GET.getlist('js_bolumler')
        js_denetim_adi = request.GET.get('js_denetim_adi')
        js_proje = request.GET.get('js_proje')
        js_rutin_planli = request.GET.get('js_rutin_planli')
        print("js rutin planlı tipi değiştiğinde okunan değer...js aldığında", js_rutin_planli)
        js_denetci = request.GET.get('js_denetci')
        js_tipi = request.GET.get('js_tipi')
        js_takipciler = request.GET.getlist('js_takipciler')
        js_hedef_baslangic = request.GET.get('js_hedef_baslangic')
        js_hedef_bitis = request.GET.get('js_hedef_bitis')
        js_aciklama = request.GET.get('js_aciklama')
        js_bolumler = []
        #js_zonlar = []
        request.session['js_bolumler'] = js_bolumler
        request.session['js_denetim_adi'] = js_denetim_adi
        request.session['js_proje'] = js_proje
        request.session['js_rutin_planli'] = js_rutin_planli
        request.session['js_denetci'] = js_denetci
        request.session['js_tipi'] = js_tipi
        request.session['js_takipciler'] = js_takipciler
        request.session['js_hedef_baslangic'] = js_hedef_baslangic
        request.session['js_hedef_bitis'] = js_hedef_bitis
        request.session['js_aciklama'] = js_aciklama
        #request.session['js_zonlar'] = js_zonlar
    print ("son nokta denetim bölüm js.....", response_data)
    return HttpResponse(response_data, content_type='application/json')

#-----------------------------------------------------------------------------------


@login_required
def teksayfa_duzenle(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Den_Olustur_Form(request.POST)

        if form.is_valid():
            print("bu form valid")
        else:
            print(" bu form is NOT VALID... nesi var kardeşim...")
        # check whether it's valid:
        if form.is_valid():
            denetim_no = request.POST.get('denetim', "")
            print(" tek sayfa düzenleden denetim no...", denetim_no)
            request.session['teksayfa_duzenle_denetim_no'] = denetim_no

            print("denetim ", denetim_no)
            denetim_obj = denetim.objects.get(id=denetim_no)
            #denetim_no = denetim_obj.id
            print("denetim objesi..", denetim_obj, "denetim no..", denetim_no)


            bolumler_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
            print("bölümler objesi...", bolumler_obj)
            takipciler_obj = sonuc_takipci.objects.filter(denetim=denetim_no)
            print("takipçiler objesi...", takipciler_obj)
            detaylar_obj = sonuc_detay.objects.filter(denetim=denetim_no)
            print("detaylar objesi...", detaylar_obj)

            js_denetim_no = denetim_obj.id
            js_denetim_adi = denetim_obj.denetim_adi
            js_proje = denetim_obj.proje.id
            js_rutin_planli = denetim_obj.rutin_planli
            js_denetci = denetim_obj.denetci.id
            js_tipi = denetim_obj.tipi.id
            js_hedef_baslangic = denetim_obj.hedef_baslangic
            js_hedef_bitis = denetim_obj.hedef_bitis
            js_aciklama = denetim_obj.aciklama

            print("denetim no", js_denetim_no)
            print("denetim adi", js_denetim_adi)
            print("proje", js_proje)
            print("rutin planlı", js_rutin_planli)
            print("denetci", js_denetci)
            print("tipi", js_tipi)
            print("hedef başlangıç", js_hedef_baslangic)
            print("hedef bitiş", js_hedef_bitis)
            print("aciklama", js_aciklama)


            bolumler = []
            i = 0
            for bolum in bolumler_obj:
                bolumler.append(bolum.bolum.id)
                i = i + 1
            print("bölümler...", bolumler)
            takipciler = []
            i = 0
            for takipci in takipciler_obj:
                takipciler.append(takipci.takipci.id)
                i = i + 1

            print("takipciler", takipciler)

            detaylar = []
            i = 0
            for detay in detaylar_obj:
                detaylar.append(detay.detay.id)
                i = i + 1

            print("detaylar", detaylar)

            js_bolumler = bolumler
            js_takipciler = takipciler
            js_detaylar = detaylar
            bolum_listesi = js_bolumler
            str_baslangic = str(js_hedef_baslangic)
            str_bitis = str(js_hedef_bitis)
            print("str başlangıç...", str_baslangic)
            print("str bitis", str_bitis)

            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            #request.session['bolum_listesi'] = bolum_listesi
            request.session['duz_js_pk_no'] = denetim_no
            request.session['duz_js_bolumler'] = js_bolumler
            request.session['duz_js_denetim_adi'] = js_denetim_adi
            request.session['duz_js_proje'] = js_proje
            request.session['duz_js_rutin_planli'] = js_rutin_planli
            request.session['duz_js_denetci'] = js_denetci
            request.session['duz_js_tipi'] = js_tipi
            request.session['duz_js_takipciler'] = js_takipciler
            #request.session['js_hedef_baslangic'] = js_hedef_baslangic
            #request.session['js_hedef_bitis'] = js_hedef_bitis
            request.session['duz_js_hedef_baslangic'] = str_baslangic
            request.session['duz_js_hedef_bitis'] = str_bitis
            request.session['duz_js_aciklama'] = js_aciklama
            request.session['duz_js_detaylar'] = js_detaylar
            request.session['ilk_duzeltme'] = True
            print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
            return redirect('teksayfa_duzenle_devam')
        else:
            #messages.success(request, 'Formda uygunsuzluk var....')
            #return redirect('denetim_create')
            denetim_no = request.POST.get('denetim', "")
            print(" tek sayfa düzenleden denetim no.AMA NOT VALID.....", denetim_no)
            return render(request, 'islem/denetim_deneme_form.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        #selected_alt = request.session.get('selected_alt')
        form = Den_Olustur_Form()
        return render(request, 'islem/denetim_deneme_form.html', {'form': form,})

#--------------------------------------------------------------------------------


@login_required
@transaction.atomic
def teksayfa_duzenle_devam(request, pk=None):
    denetim_no = request.session.get('teksayfa_duzenle_denetim_no')
    print("tek sayfa düzenle devam içinden denetim no...", denetim_no)

    if request.method == "POST":
        bolum_listesi = request.session.get('duz_js_bolumler', None)
        print("bölüm listesi...", bolum_listesi)
        init_param = False
        form = DenetimForm(request.POST or None, bolum_listesi=bolum_listesi)

        if form.is_valid():
            print(" form is valid..")
        else:
            print("form is NOT valid")

        if form.is_valid():
            print("neyse ki valid..tek sayfa düzenle devam .. artık düzenleyip  kaydediyor...")
            dd_pk_no = request.POST.get('pk_no', "")
            dd_denetim_adi = request.POST.get('denetim_adi', "")
            dd_proje =  request.POST.get('proje', "")
            dd_rutin_planli = request.POST.get('rutin_planli', "")
            dd_denetci = request.POST.get('denetci', "")
            dd_tipi =  request.POST.get('tipi', "")
            dd_takipciler = request.POST.getlist('takipciler', "")
            dd_hedef_baslangic =  request.POST.get('hedef_baslangic', "")
            dd_hedef_bitis = request.POST.get('hedef_bitis', "")
            dd_aciklama =  request.POST.get('aciklama', "")
            dd_bolum = request.POST.getlist('bolum', "")
            dd_detay = request.POST.getlist('detay', "")
            if dd_rutin_planli == "R":
                dd_hedef_baslangic = "2000-01-01"
                dd_hedef_bitis = "2000-01-01"

            print("pk no", dd_pk_no)
            print("denetim adı", dd_denetim_adi)
            print("proje", dd_proje)
            print("rutin/planlı", dd_rutin_planli)
            print("denetci", dd_denetci)
            print("tipi", dd_tipi)
            print("takipciler", dd_takipciler)
            print("hedef_baslangic", dd_hedef_baslangic)
            print("hedef_bitis", dd_hedef_bitis)
            print("açıklama", dd_aciklama)
            print("bolum", dd_bolum)
            print("detay", dd_detay)

            # mailler için eski objeler alınıyor....

            eskidenetim_obj = denetim.objects.get(id=dd_pk_no)
            eski_denetci = eskidenetim_obj.denetci
            eski_denetci_adi = eskidenetim_obj.denetci.get_full_name()
            eski_hbaslangic = eskidenetim_obj.hedef_baslangic
            eski_hbitis = eskidenetim_obj.hedef_bitis

            eski_takipciler_obj = sonuc_takipci.objects.filter(denetim=dd_pk_no)
            eski_takipci_list = []
            for takipci in eski_takipciler_obj:
                eski_takipci_list.append(takipci.takipci)

            eski_bolum_obj = sonuc_bolum.objects.filter(denetim=dd_pk_no)
            eski_bolum_list = []
            for bolum in eski_bolum_obj:
                eski_bolum_list.append(bolum.bolum)



            kaydetme_obj = denetim(id=dd_pk_no,
                                   denetim_adi=dd_denetim_adi,
                                   proje_id=dd_proje,
                                   rutin_planli = dd_rutin_planli,
                                   denetci_id=dd_denetci,
                                   tipi_id=dd_tipi,
                                   hedef_baslangic=dd_hedef_baslangic,
                                   hedef_bitis=dd_hedef_bitis,
                                   aciklama=dd_aciklama,
                                   yaratan=request.user
                                   )
            kaydetme_obj.save()

            denetim_obj = denetim.objects.get(id=dd_pk_no)
            print("son no. denetim.", denetim_obj.id, "denetim adı", denetim_obj.denetim_adi)
            denetim_no = denetim_obj.id

            try:
                silme_obj = sonuc_takipci.objects.filter(denetim=denetim_no)
            except ObjectDoesNotExist:
                silme_obj = None

            if silme_obj:
                silme_obj.delete()

            i = 0
            while i < len(dd_takipciler):
                print("takipciler..", dd_takipciler[i])
                kaydetme_obj = sonuc_takipci(denetim_id=dd_pk_no,
                                             takipci_id=dd_takipciler[i]
                                             )
                kaydetme_obj.save()
                i = i + 1

            try:
                silme_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
            except ObjectDoesNotExist:
                silme_obj = None

            if silme_obj:
                silme_obj.delete()


            try:
                silme_obj = sonuc_detay.objects.filter(denetim=denetim_no)
            except ObjectDoesNotExist:
                silme_obj = None

            if silme_obj:
                silme_obj.delete()



            i = 0
            while i < len(dd_bolum):
                print("bolüm listesi..:", dd_bolum[i])
                kaydetme_obj = sonuc_bolum(denetim_id=denetim_no,
                                           bolum_id=dd_bolum[i]
                                           )
                kaydetme_obj.save()
                bolum_no = int(dd_bolum[i])
                print("son no. bolum .", bolum_no)

                j = 0
                while j < len(dd_detay):
                    detay_no = int(dd_detay[j])
                    print("işte detay no...", detay_no)
                    detayli_obj = detay.objects.get(id=detay_no)
                    olmali_bolum = detayli_obj.bolum.id
                    if bolum_no == olmali_bolum:
                        kaydet_obj = sonuc_detay(denetim_id=denetim_no,
                                                    bolum_id=bolum_no,
                                                    detay_id=detay_no
                                                    )
                        kaydet_obj.save()
                    j = j + 1

                i = i + 1

            ######################################################
            #MAILLER ATILIYOR....................
            ######################################################

            #connection = mail.get_connection()
            #connection.open()

            denetci_adi = denetim_obj.denetci.get_full_name()
            denetim_id = denetim_obj.id
            denetim_adi = denetim_obj.denetim_adi
            baslangic = denetim_obj.hedef_baslangic
            bitis = denetim_obj.hedef_bitis
            denetci = denetim_obj.denetci

            takipci_obj = sonuc_takipci.objects.filter(denetim=denetim_id)
            takipci_list = []
            for takipci in takipci_obj:
                takipci_list.append(takipci.takipci)

            bolum_obj = sonuc_bolum.objects.filter(denetim=denetim_id)
            bolum_list = []
            for bolum in bolum_obj:
                bolum_list.append(bolum.bolum)



            if not (denetci == eski_denetci):

                adi = denetci_adi
                subject = "Denetim tarihlerinde değişiklikler "
                to = [denetim_obj.denetci.email]
                from_email = settings.EMAIL_HOST_USER
                ctx = {
                    'adi': adi,
                    'denetim_adi': denetim_adi,
                    'baslangic': baslangic,
                    'bitis' : bitis
                    }
                message = get_template('islem/emt_denetci_oldun.html').render(ctx)
                msg = EmailMessage(subject, message, to=to, from_email=from_email)
                msg.content_subtype = 'html'
                msg.send()


                adi = eski_denetci_adi
                subject = "Denetim tarihlerinde değişiklikler "
                to = [denetim_obj.denetci.email]
                from_email = settings.EMAIL_HOST_USER
                ctx = {
                    'adi': adi,
                    'denetim_adi': denetim_adi,
                    'baslangic': baslangic,
                    'bitis' : bitis
                    }
                message = get_template('islem/emt_denetci_iptal.html').render(ctx)
                msg = EmailMessage(subject, message, to=to, from_email=from_email)
                msg.content_subtype = 'html'
                msg.send()


            if not (eski_takipci_list == takipci_list):

                eski_set = set(eski_takipci_list)
                yeni_set = set(takipci_list)
                ortak = eski_set.intersection(yeni_set)
                cikan = list(eski_set - ortak)
                giren = list(yeni_set - ortak)

                print("çıkan", cikan)
                print("giren", giren)

                for cikan_no in cikan:
                    cikan_obj = User.objects.get(id=cikan_no)
                    adi = cikan_obj.get_full_name
                    subject = "Takipçiliğiniz kaldırıldı"
                    to = [cikan_obj.email]
                    from_email = settings.EMAIL_HOST_USER
                    ctx = {
                        'adi': adi,
                        'denetim_adi': denetim_adi
                        }
                    message = get_template('islem/emt_takipci_iptal.html').render(ctx)
                    msg = EmailMessage(subject, message, to=to, from_email=from_email)
                    msg.content_subtype = 'html'
                    msg.send()

                for giren_no in giren:
                    giren_obj = User.objects.get(id=giren_no)
                    adi = giren_obj.get_full_name
                    subject = "Takipçi olarak atandınız"
                    to = [giren_obj.email]
                    from_email = settings.EMAIL_HOST_USER
                    ctx = {
                        'adi': adi,
                        'denetim_adi': denetim_adi,
                        'baslangic': baslangic,
                        'bitis': bitis
                        }
                    message = get_template('islem/emt_takipci_oldun.html').render(ctx)
                    msg = EmailMessage(subject, message, to=to, from_email=from_email)
                    msg.content_subtype = 'html'
                    msg.send()


            if not ((baslangic == eski_hbaslangic) and (bitis == eski_hbitis)):

                adi = denetci_adi
                subject = "Denetim tarihlerinde değişiklikler "
                to = [denetim_obj.denetci.email]
                from_email = settings.EMAIL_HOST_USER
                ctx = {
                    'adi': adi,
                    'denetim_adi': denetim_adi,
                    'baslangic': baslangic,
                    'bitis' : bitis
                    }
                message = get_template('islem/emt_tarih_degisti.html').render(ctx)
                msg = EmailMessage(subject, message, to=to, from_email=from_email)
                msg.content_subtype = 'html'
                msg.send()

                takipci_obj = sonuc_takipci.objects.filter(denetim=denetim_id)

                for takipci in takipci_obj:
                    adi = takipci.takipci.get_full_name()
                    subject = "Denetim tarihlerinde değişiklikler"
                    to = [takipci.takipci.email]
                    from_email = settings.EMAIL_HOST_USER
                    ctx = {
                        'adi': adi,
                        'denetim_adi': denetim_adi,
                        'baslangic': baslangic,
                        'bitis' : bitis
                        }
                    message = get_template('islem/emt_tarih_degisti.html').render(ctx)
                    msg = EmailMessage(subject, message, to=to, from_email=from_email)
                    msg.content_subtype = 'html'
                    msg.send()

            if not (eski_bolum_list == bolum_list):

                adi = denetci_adi
                subject = "Denetim bölümlerinde değişiklikler "
                to = [denetim_obj.denetci.email]
                from_email = settings.EMAIL_HOST_USER
                ctx = {
                    'adi': adi,
                    'denetim_adi': denetim_adi,
                    'baslangic': baslangic
                    }
                message = get_template('islem/emt_bolum_degisti.html').render(ctx)
                msg = EmailMessage(subject, message, to=to, from_email=from_email)
                msg.content_subtype = 'html'
                msg.send()

                takipci_obj = sonuc_takipci.objects.filter(denetim=denetim_id)

                for takipci in takipci_obj:
                    adi = takipci.takipci.get_full_name()
                    subject = "Denetim bölümlerinde değişiklikler"
                    to = [takipci.takipci.email]
                    from_email = settings.EMAIL_HOST_USER
                    ctx = {
                        'adi': adi,
                        'denetim_adi': denetim_adi,
                        'baslangic': baslangic
                        }
                    message = get_template('islem/emt_bolum_degisti.html').render(ctx)
                    msg = EmailMessage(subject, message, to=to, from_email=from_email)
                    msg.content_subtype = 'html'
                    msg.send()

            #connection.close()
            #-----------------------------------------------------------------
            # EMAIL işlemleri tamamlandı.......................................


            request.session['js_bolumler'] = None
            request.session['js_denetim_adi'] = None
            request.session['js_proje'] = None
            request.session['js_rutin_planli'] = None
            request.session['js_denetci'] = None
            request.session['js_tipi'] = None
            request.session['js_takipciler'] = None
            request.session['js_hedef_baslangic'] = None
            request.session['js_hedef_bitis'] = None
            request.session['js_aciklama'] = None
            messages.success(request, 'denetim başarıyla kaydedildi')
            #return render(request, 'islem/tek_sayfa.html', context,)
            return redirect('index')
        else:
            print("ne oldu be kardeşim2...........")
            messages.success(request, ' form hatası - tekrar deneyin')
            return redirect('teksayfa_duzenle_devam')
            #return render(request, 'islem/denetim_bolum_sec.html', {'form': form,})


    else:
        print("get get get get get get ..................................")

        # yaratma ile aynı mantıkta olmalı....
        # yani bir kere yükle ...veri tabanından
        # sonra ne değişiklik varsa devam et....

        # yukarıda veri tabanından yükleyecek burada ise bölümler js den gelecek ve
        # buna göre yükleme yapacak seçerek, diğerleri de  js den gelecek....
        # sadece detayları özel olarak sececek....
        # kaydetme isini posta bırakarak....


        js_denetim_no = request.session.get('duz_js_pk_no', None)
        js_denetim_adi = request.session.get('duz_js_denetim_adi', None)
        js_proje = request.session.get('duz_js_proje', None)
        js_rutin_planli = request.session.get('duz_js_rutin_planli', None)
        js_denetci = request.session.get('duz_js_denetci', None)
        js_tipi = request.session.get('duz_js_tipi', None)
        js_takipciler = request.session.get('duz_js_takipciler', None)
        js_hedef_baslangic = request.session.get('duz_js_hedef_baslangic', None)
        js_hedef_bitis = request.session.get('duz_js_hedef_bitis', None)
        js_aciklama = request.session.get('duz_js_aciklama', None)
        js_bolumler = request.session.get('duz_js_bolumler', None)
        js_detaylar = request.session.get('duz_js_detaylar', None)
        ilk_duzeltme = request.session.get('ilk_duzeltme', None)
        print("denetim no", js_denetim_no)
        print("denetim adi", js_denetim_adi)
        print("proje", js_proje)
        print("rutin/planlı", js_rutin_planli)
        print("denetci", js_denetci)
        print("tipi", js_tipi)
        print("hedef başlangıç", js_hedef_baslangic)
        print("hedef bitiş", js_hedef_bitis)
        print("aciklama", js_aciklama)
        print("bölümler", js_bolumler)
        print("detaylar", js_detaylar)
        bolum_listesi = js_bolumler

        if ilk_duzeltme:
            init_param = False
            request.session[ilk_duzeltme] = False
        else:
            init_param = True

        form = DenetimForm(bolum_listesi=bolum_listesi)
        form.fields["pk_no"].initial = js_denetim_no
        form.fields["denetim_adi"].initial = js_denetim_adi
        form.fields["proje"].initial = js_proje
        form.fields["rp_hidden"].initial = js_rutin_planli
        print("düzeltme init içinden js rutin planlı...", js_rutin_planli)
        form.fields["denetci"].initial = js_denetci
        form.fields["tipi"].initial = js_tipi
        form.fields["takipciler"].initial = js_takipciler
        form.fields["hedef_baslangic"].initial = js_hedef_baslangic
        form.fields["hedef_bitis"].initial = js_hedef_bitis
        form.fields["aciklama"].initial = js_aciklama
        form.fields["bolum"].initial = js_bolumler
        form.fields["detay"].initial = js_detaylar
        context = { 'form': form, }
        return render(request, 'islem/tek_sayfa_duzenle.html', context,)


#---------------------------------------------------------------------------------------


def detaylarsec_bolum_js_2(request, pk=None):
    print("selam buraya geldik...detaylarseç 222222 bölüm js")
    print("User.id.....:", request.user.id)
    kullanan = request.user.id
    response_data ={}
    if request.method == 'GET':
        denetim_no = request.GET.get('js_pk_no')
        js_bolumler = request.GET.getlist('js_bolumler')
        js_denetim_adi = request.GET.get('js_denetim_adi')
        js_proje = request.GET.get('js_proje')
        js_rutin_planli = request.GET.get('js_rutin_planli')
        js_denetci = request.GET.get('js_denetci')
        js_tipi = request.GET.get('js_tipi')
        js_takipciler = request.GET.getlist('js_takipciler')
        js_hedef_baslangic = request.GET.get('js_hedef_baslangic')
        js_hedef_bitis = request.GET.get('js_hedef_bitis')
        js_aciklama = request.GET.get('js_aciklama')

        # bölümlerin eskilerini silip yenilerini yazıyor mutlaka...
        # sonra da sayfa yeniden yükleniyor, böylece deyatlar istendiği gibi geliyor...
        # ama save etmeden bile bölüm ve detaylarda değişiklik yapılmış oluyor....
        # bu anlamda doğru değil....
        # düşünmek lazım....
        # yazmaması lazım.....sadece parametre aktarmalı....
        #---------------------------------

        request.session['duz_js_pk_no'] = denetim_no
        request.session['duz_js_bolumler'] = js_bolumler
        request.session['duz_js_denetim_adi'] = js_denetim_adi
        request.session['duz_js_proje'] = js_proje
        request.session['duz_js_rutin_planli'] = js_rutin_planli
        request.session['duz_js_denetci'] = js_denetci
        request.session['duz_js_tipi'] = js_tipi
        request.session['duz_js_takipciler'] = js_takipciler
        request.session['duz_js_hedef_baslangic'] = js_hedef_baslangic
        request.session['duz_js_hedef_bitis'] = js_hedef_bitis
        request.session['duz_js_aciklama'] = js_aciklama

    print ("son nokta denetim bölüm js.....", response_data)
    return HttpResponse(response_data, content_type='application/json')


#---------------------------------------------------------------------------------------

def tipisec_bolum_js_2(request, pk=None):
    print("selam buraya geldik...tipiseç 222222 bölüm js")
    print("User.id.....:", request.user.id)
    kullanan = request.user.id
    response_data ={}
    if request.method == 'GET':
        denetim_no = request.GET.get('js_pk_no')
        js_bolumler = request.GET.getlist('js_bolumler')
        js_denetim_adi = request.GET.get('js_denetim_adi')
        js_proje = request.GET.get('js_proje')
        js_rutin_planli = request.GET.get('js_rutin_planli')
        js_denetci = request.GET.get('js_denetci')
        js_tipi = request.GET.get('js_tipi')
        js_takipciler = request.GET.getlist('js_takipciler')
        js_hedef_baslangic = request.GET.get('js_hedef_baslangic')
        js_hedef_bitis = request.GET.get('js_hedef_bitis')
        js_aciklama = request.GET.get('js_aciklama')
        js_bolumler = []

        request.session['bolum_listesi'] = js_bolumler
        request.session['duz_js_bolumler'] = js_bolumler
        request.session['duz_js_denetim_adi'] = js_denetim_adi
        request.session['duz_js_proje'] = js_proje
        request.session['duz_js_rutin_planli'] = js_rutin_planli
        request.session['duz_js_denetci'] = js_denetci
        request.session['duz_js_tipi'] = js_tipi
        request.session['duz_js_takipciler'] = js_takipciler
        request.session['duz_js_hedef_baslangic'] = js_hedef_baslangic
        request.session['duz_js_hedef_bitis'] = js_hedef_bitis
        request.session['duz_js_aciklama'] = js_aciklama
        request.session['duz_js_pk_no'] = denetim_no

    print ("son nokta denetim bölüm js.....", response_data)
    return HttpResponse(response_data, content_type='application/json')


#---------------------------------------------------------------------

@login_required
def teksayfa_sil(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Den_Olustur_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            denetim_no = request.POST.get('denetim', "")
            print(" tek sayfa silden denetim no...", denetim_no)
            request.session['teksayfa_sil_denetim_no'] = denetim_no

            denetim_obj = denetim.objects.get(id=denetim_no)
            print("seçilen denetim", denetim_obj)
            denetim_adi = denetim_obj.denetim_adi
            proje = denetim_obj.proje
            rutin_planli = denetim_obj.rutin_planli
            denetci = denetim_obj.denetci
            tipi = denetim_obj.tipi
            yaratim_tarihi = denetim_obj.yaratim_tarihi
            yaratan = denetim_obj.yaratan
            hedef_baslangic = denetim_obj.hedef_baslangic
            hedef_bitis = denetim_obj.hedef_bitis
            gerc_baslangic = denetim_obj.gerc_baslangic
            gerc_bitis = denetim_obj.gerc_bitis
            durum = denetim_obj.durum
            takipci_obj = sonuc_takipci.objects.filter(denetim=denetim_no)
            print("takipci objesi...", takipci_obj)
            i = 0
            takipciler = []
            for takipci in takipci_obj:
                takipciler.append(takipci.takipci)
                i = i + 1
            print("takipciler listesi..", takipciler)
            d = collections.defaultdict(list)
            bolum_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
            for bolum in bolum_obj:
                print("bolum list . bolum", bolum.bolum)
                detay_obj = sonuc_detay.objects.filter(denetim=denetim_no, bolum=bolum.bolum)
                for detay in detay_obj:
                    print("detay list . detay", detay.bolum, detay.detay)
                    d[detay.bolum].append(detay.detay)
            print("***********************")
            print(d)
            d.default_factory = None
            dict_bol_detay = dict(d)
            print("************************")
            print(dict_bol_detay)
            context = {'dict_bol_detay':dict_bol_detay,
                        'takipciler': takipciler,
                        'denetim_adi': denetim_adi,
                        'proje' : proje,
                        'rutin_planli' : rutin_planli,
                        'denetci' : denetci,
                        'tipi' : tipi,
                        'yaratim_tarihi' : yaratim_tarihi,
                        'yaratan' : yaratan,
                        'hedef_baslangic' : hedef_baslangic,
                        'hedef_bitis' : hedef_bitis,
                        'durum' : durum,
                        }
            return render(request, 'islem/teksayfa_sil_soru.html', context )


        else:
            #messages.success(request, 'Formda uygunsuzluk var....')
            #return redirect('denetim_create')
            return render(request, 'islem/denetim_deneme_form.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        #selected_alt = request.session.get('selected_alt')
        form = Den_Olustur_Form()
        return render(request, 'islem/denetim_deneme_form.html', {'form': form,})



@login_required
def teksayfa_sil_kesin(request, pk=None):
    denetim_no = request.session.get('teksayfa_sil_denetim_no')
    print("denetim sil kesindeki  denetim no:", denetim_no)
    object = denetim.objects.get(id=denetim_no)
    object.durum = "X"
    object.save()
#********************************************************
#....  ilgili kişilere e-posta gönder.....................
#.........................................................
    denetim_obj = denetim.objects.get(id=denetim_no)

    #connection = mail.get_connection()
    #connection.open()

    adi = denetim_obj.denetci.get_full_name()
    denetim_id = denetim_obj.id
    denetim_adi = denetim_obj.denetim_adi
    baslangic = denetim_obj.hedef_baslangic
    bitis = denetim_obj.hedef_bitis

    subject = "Denetim iptal edildi"
    to = [denetim_obj.denetci.email]
    from_email = settings.EMAIL_HOST_USER
    ctx = {
        'adi': adi,
        'denetim_adi': denetim_adi,
        'baslangic': baslangic
        }
    message = get_template('islem/emt_denetim_iptal.html').render(ctx)
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

    takipci_obj = sonuc_takipci.objects.filter(denetim=denetim_id)

    for takipci in takipci_obj:
        adi = takipci.takipci.get_full_name()
        subject = "Denetim iptal edildi"
        to = [takipci.takipci.email]
        from_email = settings.EMAIL_HOST_USER
        ctx = {
            'adi': adi,
            'denetim_adi': denetim_adi,
            'baslangic': baslangic
            }
        message = get_template('islem/emt_denetim_iptal.html').render(ctx)
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()

    #connection.close()

    messages.success(request, 'Başarıyla silindi')
    return redirect('index')











#-------------------------------------------------------------------------------

# js içinden tamam butonu ile çalışıyor...
# bölüm seçildiğinde bu bölümde detay var mı diye bakıp
# sonrasında bu bölümdeki tüm detaylar H yapıp detayları sifirlıyor...

@login_required
def detay_islemleri_baslat(request, pk=None):
    print("denetim  detay işlemleri başlat... jquery den gelen..")
    response_data ={}
    if request.method == 'GET':
        denetim_no = request.session.get('denetim_no')
        secili_bolum = request.session.get('secili_bolum')
        # selected = request.GET.get('selected', None)
        print("denetim no...:", denetim_no )
        print("secili bolum...", secili_bolum)
        ilk_detaylar = sonuc_detay.objects.filter(denetim=denetim_no)
        print("ilk detaylar..:", ilk_detaylar)
        detaylar = ilk_detaylar.filter(bolum=secili_bolum)
        print("detaylar..:", detaylar)
        if not detaylar:
            messages.success(request, 'Seçili bölümde bölüm detayı yok')
            return redirect('denetim_baslat')
        for detay in detaylar:
            print("bolum id for loop içinden", detay.bolum.id, "ve detay id", detay.detay.id)
            detay.tamam = "H"
            detay.save()
        return HttpResponse(response_data, content_type='application/json')



#--------------------------------------------------------------------------------

# denetim esnasında sahada işlemin yapıldığı yer....
# bölümü seçiyor, sonrasında sırayla gelen detaylara cevap veriyor...
# sonunda bölüm tamamlanıyor ve tekrar bölüm seçe geliniyor...
# bölümler tamamlandıysa denetimi kapatmak istiyor musunuz diye soruyor...

# tamamladığı denetimleri tekrar değiştirmek istiyorsa da olmalı..???????
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render


#@csrf_protect
@login_required
def denetim_detay_islemleri(request, pk=None):


    # if this is a POST request we need to process the form data
    denetim_no = request.session.get('denetim_no')
    secili_bolum = request.session.get('secili_bolum')
    secili_detay = request.session.get('secili_detay')
    print("denetim detay işlemleri...................")
    print("denetim_no", denetim_no)
    print("secili_bolum", secili_bolum)
    print("secili_detay", secili_detay)


    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        print("buraya mı geldi...  denetim_detay işlemleri...POST")
        secili_detay_obje_id = request.session.get('secili_detay_obje_id')
        print("secili detay obje id, get tarafında kaydedilen...", secili_detay_obje_id)
        detay_obj = sonuc_detay.objects.get(id=secili_detay_obje_id)
        print("detay obj...", detay_obj.id, "adııı", detay_obj.detay.detay_adi)
        form = SonucForm(request.POST or None, instance=detay_obj)
        #form = SonucForm(request.POST or None)
        if form.is_valid():
            print("neyse ki valid..bin...ext...")
            # bu detay için tamamı E yap, yani tamamlandı....sonra update yap...
            form_one = form.save(commit=False)

            puanlama_turu = form_one.puanlama_turu
            print("puanlama türü...", form_one.puanlama_turu)
            if form_one.denetim_disi == "H":
                if puanlama_turu == "A":
                    puan_hesap = int(form_one.onluk)
                if puanlama_turu == "B":
                    puan_hesap = int(form_one.beslik)
                    puan_hesap = puan_hesap * 2
                if puanlama_turu == "C":
                    puan_hesap = int(form_one.ikilik)
                    puan_hesap = puan_hesap * 10
                form_one.puan = puan_hesap

            form_one.tamam = "E"
            form_one.save()


            print("form one kaydet sonrası")
            # denetim dışı bilgisi gelirse resimlerin hepsini sil......
            if form_one.denetim_disi == "E":
                print(" form one denetim dışı ==  evet olmuş...")
                resimler_obj = sonuc_resim.objects.filter(sonuc_detay=pk)
                print("işte silinecek resimler...", resimler_obj)
                if resimler_obj:
                    for resim in resimler_obj:
                        print("silinecek resmin id si...", resim.id)
                        resim.delete()

            print("kaydetmiş olması lazım.................")

            # bir sonraki................
            # için  işlem yap................
            ilk_detaylar = sonuc_detay.objects.filter(denetim=denetim_no)
            print("ilk detaylar..denetim detay işlemleri :", ilk_detaylar)
            detaylar = ilk_detaylar.filter(bolum=secili_bolum)
            print("detaylar.. denetim detay işlemleri..:", detaylar)
            secili_detay_obj = detaylar.filter(tamam="H")
            for dty in secili_detay_obj:
                print("seçili detaylar tamam H olanlar...", dty.detay.detay_adi, "---tamam---", dty.tamam)

            if not secili_detay_obj:
                # sonuc_bolum dosyasında tamamlandıyı E yap bölüm bitmiş olsun....
                ilk_sonuc_bolum = sonuc_bolum.objects.filter(denetim=denetim_no)
                print("sonuc bölüm ilk....", ilk_sonuc_bolum)
                sec_bolum = get_object_or_404(ilk_sonuc_bolum, bolum=secili_bolum)
                print(" seçili bölüm sonuc_bolum içinden ", sec_bolum)
                sec_bolum.tamam = "E"
                sec_bolum.save()
                devam_tekrar = request.session.get('devam_tekrar')
                if devam_tekrar == "devam":
                    messages.success(request, 'Bölüm içindeki denetim detay işlemleri tamamlandı')
                    request.session['bolum_atla_flag'] = False
                    return redirect('denetim_bolum_sec')
                else:
                    messages.success(request, 'Bölüm içindeki denetim detay işlemleri tamamlandı')
                    return redirect('devam_liste')
            """
            secili_obj = secili_detay_obj.first()
            secili_detay_id = secili_obj.detay.id
            print("secili - detay.... bakalım  doğru mu...", secili_detay_id)
            request.session['secili_detay'] = secili_detay_id

            detay_resim_obj = sonuc_resim.objects.filter(sonuc_detay=secili_detay_id)
            print("detay resimleri kaç taneyde...", detay_resim_obj)

            form = SonucForm(instance=secili_obj)

            context = { 'form': form,
                        #'formset': formset,
                        'secili_obj' : secili_obj,
                        'detay_resim_obj': detay_resim_obj,
                        }
            return render(request, 'islem/denetim_detay_islemleri.html', context,)
            """
            return redirect('denetim_detay_islemleri')

        else:
            print(form.errors)
            return render(request, 'islem/denetim_detay_islemleri.html')


    # if a GET (or any other method) we'll create a blank form
    else:
        print("denetim detay işlemleri...GETTTTTT")
        ilk_detaylar = sonuc_detay.objects.filter(denetim=denetim_no)
        print("ilk detaylar..denetim detay işlemleri :", ilk_detaylar)
        detaylar = ilk_detaylar.filter(bolum=secili_bolum)
        print("detaylar.. denetim detay işişlemleri..:", detaylar)
        secili_detay_obj = detaylar.filter(tamam="H")
        print("seçili detaylar tamam H olanlar...", secili_detay_obj)

        if not secili_detay_obj:
            messages.success(request, 'Bölüm içinde detay işlemleri tamamlandı')
            request.session['bolum_atla_flag'] = False
            return redirect('denetim_bolum_sec')
        secili_obj = secili_detay_obj.first()
        secili_detay_id = secili_obj.detay.id
        request.session['sonuc_detay_id'] = secili_obj.id

        print("secili - detay.... bakalım  doğru mu...", secili_detay_id)
        print("seçili obje ise ayrı...", secili_obj.id)
        request.session['secili_detay'] = secili_detay_id
        request.session['secili_detay_obje_id'] = secili_obj.id
        detay_resim_obj = sonuc_resim.objects.filter(sonuc_detay=secili_obj.id)
        print("detay resimleri kaç taneyde...", detay_resim_obj)

        form = SonucForm(instance=secili_obj)

        context = { 'form': form,
                    #'formset': formset,
                    'secili_obj' : secili_obj,
                    'detay_resim_obj': detay_resim_obj,
                    }

        return render(request, 'islem/denetim_detay_islemleri.html', context,)



#------------------------------------------------------
#  tamamlanmış denetimlerin sonuçlarını görmek için öncelikle tamamlanmış denetimleri seç
#  şu an için devam eden denetimleri de gözlemliyor....B ve C durumu...fakat sadece D lere bakacak...
#-----------------------------------------------------

@login_required
def sonuc_denetim_sec(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        #denetim_obj_ilk = denetim.objects.filter(durum="B") | denetim.objects.filter(durum="C")
        #denetim_obj = denetim_obj_ilk.filter(denetci=request.user)
        print("post içinden form yüklemeden önce...............")
        denetci=request.user
        form = DuzenleDenetimSecForm(request.POST, denetci=denetci)
        # check whether it's valid:
        if form.is_valid():
            denetim_no = request.POST.get('denetim_no', "")
            print ("denetim seçim yapılmış...", denetim_no)
            request.session['secilen_denetim'] = denetim_no
            return redirect('sonuc_denetim_sec_dogrudan', pk_den=denetim_no)
            """
            denetim_obj = denetim.objects.get(id=denetim_no)
            if rapor_verisi_hazirla(request, denetim_no=denetim_no):
                sonuc_detay_list = sonuc_detay.objects.filter(denetim=denetim_no).order_by('id')
                sonuc_bolum_list = sonuc_bolum.objects.filter(denetim=denetim_no).order_by('id')
                context = {'sonuc_detay_list': sonuc_detay_list,
                           'sonuc_bolum_list': sonuc_bolum_list,
                           'denetim_obj': denetim_obj}
                return render(request, 'islem/sonuc_list.html', context)
            else:
                mesaj = request.session.get('mesaj_rapor_verisi')
                return render(request, 'islem/uyari.html', {'mesaj': mesaj})
            """
        else:
            #form = DenetimSecForm()
            return render(request, 'islem/ana_menu.html',)

    # if a GET (or any other method) we'll create a blank form
    else:
        #denetim_obj_ilk = denetim.objects.filter(durum="C") | denetim.objects.filter(durum="D")
        # buradan C kalkacak sadece D kalacak..............
        #denetim_obj = denetim_obj_ilk.filter(denetci=request.user)
        #if denetim_obj:
        #print("get çalıştı..................", denetim_obj)
        denetci=request.user
        form = DuzenleDenetimSecForm(denetci=denetci)
        return render(request, 'islem/sonuc_denetim_form.html', {'form': form,})



@login_required
def sonuc_denetim_sec_dogrudan(request, pk_den=None):
    denetim_no = pk_den
    denetim_obj = denetim.objects.get(id=denetim_no)
    if rapor_verisi_hazirla(request, denetim_no=denetim_no):
        sonuc_detay_list = sonuc_detay.objects.filter(denetim=denetim_no).order_by('id')
        sonuc_bolum_list = sonuc_bolum.objects.filter(denetim=denetim_no).order_by('id')
        context = {'sonuc_detay_list': sonuc_detay_list,
                   'sonuc_bolum_list': sonuc_bolum_list,
                   'denetim_obj': denetim_obj}
        return render(request, 'islem/sonuc_list.html', context)
    else:
        mesaj = request.session.get('mesaj_rapor_verisi')
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})



@login_required
def sonuc_denetim_detay_sec(request, pk_den=None, pk=None):
    # if this is a POST request we need to process the form data
    pk = pk
    print("gelen pk...", pk)
    denetim_no = request.session.get('secilen_denetim')
    print("seçilen denetim...", denetim_no)
    sonuc_list = sonuc_detay.objects.filter(denetim=denetim_no).order_by('id')
    secili_detay = sonuc_detay.objects.filter(id=pk).first()

    for sonuc in sonuc_list:
        print("sonuç list id leri....", sonuc.id)

    prev_issue = (sonuc_list.filter(id__lt=secili_detay.id).last())
    next_issue = (sonuc_list.filter(id__gt=secili_detay.id).first())
    if prev_issue:
        print("previous..", prev_issue.id)
    if next_issue:
        print("next...", next_issue.id)

    context = {'secili_detay': secili_detay,
                'prev_issue': prev_issue,
                'next_issue': next_issue,
                'denetim_no': denetim_no}

    return render(request, 'islem/sonuc_detay_yeni_detail.html', context)





#ÇALIŞILAN ......................
from django.forms import modelformset_factory

@login_required
def sonuc_denetim_detay_duzenle(request, pk_den=None, pk=None):
    # if this is a POST request we need to process the form data
    pk = pk
    print("gelen pk...", pk)
    request.session['sonuc_detay_id'] = pk

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        print("buraya mı geldi...sonuç denetim detay düzenle...POST")
        #bulunan = get_object_or_404(sonuc, detay=secili_detay)
        detay_obj = sonuc_detay.objects.filter(id=pk).first()
        puanlama_turu = detay_obj.puanlama_turu
        denetim_no = detay_obj.denetim.id
        form = SonucForm(request.POST or None, instance=detay_obj)
        #formset = ResimFormSet(request.POST, request.FILES, queryset=resim_detay.objects.none())

        if form.is_valid():
            form_one = form.save(commit=False)
            puanlama_turu = form_one.puanlama_turu
            if puanlama_turu == "A":
                puan_hesap = int(form_one.onluk)
            if puanlama_turu == "B":
                puan_hesap = int(form_one.beslik)
                puan_hesap = puan_hesap * 2
            if puanlama_turu == "C":
                puan_hesap = int(form_one.ikilik)
                puan_hesap = puan_hesap * 10
            form_one.puan = puan_hesap
            form_one.tamam = "E"
            form_one.save()


            # denetim dışı bilgisi gelirse resimlerin hepsini sil......
            if form_one.denetim_disi == "E":
                print(" form one denetim dışı ==  evet olmuş...")
                resimler_obj = sonuc_resim.objects.filter(sonuc_detay=pk)
                print("işte silinecek resimler...", resimler_obj)
                if resimler_obj:
                    for resim in resimler_obj:
                        print("silinecek resmin id si...", resim.id)
                        resim.delete()

            if not(rapor_verisi_hazirla(request, denetim_no=denetim_no)):
                mesaj = "Rapor verisi hazırlanamadı..."
                return render(request, 'islem/uyari.html', {'mesaj': mesaj})

            return redirect('sonuc_denetim_detay_sec', pk_den=pk_den, pk=pk)

        else:
            print(form.errors)
            return render(request, 'islem/sonuc_detay_duzenle.html',)
    else:

        detay_obj = sonuc_detay.objects.filter(id=pk).first()
        print("detay obje olmalı - ......", detay_obj)
        detay_resim_obj = sonuc_resim.objects.filter(sonuc_detay=pk)
        print("detay resimleri kaç taneyde...", detay_resim_obj)

        form = SonucForm(instance=detay_obj)

        context = { 'form': form,
                    #'formset': formset,
                    'secili_obj' : detay_obj,
                    'detay_resim_obj': detay_resim_obj,
                    }

        return render(request, 'islem/sonuc_detay_duzenle.html', context,)






#--------------------------------------------------------------------------------
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@login_required
def update_resim_varmi(request, pk=None):
    print("selam buraya geldik...update resim var mı")
    response_data ={}
    if request.method == 'GET':
        degisken = request.GET.get('degisken')
        request.session['resim_varmi'] = degisken
        print("  js içinden  okunan değer....",  degisken)
        print ("  resim var mı sv nin son hali.....", request.session['resim_varmi'])
    return HttpResponse(response_data, content_type='application/json')




@csrf_exempt
@login_required
def getvalue_resim_varmi(request, pk=None):
    print("selam buraya geldik...getvalue resim var mı")
    response_data ={}
    data =  request.session.get('resim_varmi')
    print("  js içinden  okunan değer....",  data)
    response_data = {'data': data}
    return HttpResponse(json.dumps(data), content_type='application/json')


#-----------------------------------------------------------------------------------------------


from django.views.decorators.csrf import csrf_exempt


@login_required
@csrf_exempt

def kucuk_resim_yaz(request, pk_den=None, pk=None):
    print("selam buraya geldik.... küçük resim yaz...")
    response_data ={}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        print("buraya mı geldi...küçük resim al.............POST")
        js_sonuc_detay = request.POST.get('sonuc_detay')
        js_foto = request.POST.get('form_data')
        bir = sonuc_resim.objects.create(sonuc_detay=js_sonuc_detay, foto="")
        form = SonucResimForm(request.POST or None, request.FILES or None, instance=bir)
        if form.is_valid():
            print(" gelen resim valid......")
            kaydet = form.save(commit=False)
            kaydet.save()
            print("kaydetmiş olması lazım.................")
        else:
            print("bu ibnenin nesi valid değil anlamadım ki......")
    print ("son nokta  küçük resim al....", response_data)
    return HttpResponse(response_data, content_type='application/json')


@login_required
@csrf_exempt
def kucuk_resim_al(request, pk_den=None, pk=None):
    print("selam buraya geldik.... küçük resim al...")
    response_data ={}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        print("buraya mı geldi...küçük resim al.............POST")
        if kucukresim.objects.filter(kullanici=request.user.id).exists():
            print("bu  kullanıcı için küçük resim alanı var...")
        else:
            kaydetme_obj = kucukresim(kullanici_id=request.user.id, foto_kucuk="",)
            kaydetme_obj.save()
            print("bu kullanıcı için yeni küçük resim alanı yaratıldı...")
        bir = kucukresim.objects.get(kullanici=request.user.id)
        print("şu anki yüklü küçük resim......:", bir.foto_kucuk)
        form = KucukResimForm(request.POST or None, request.FILES or None, instance=bir)
        if form.is_valid():
            print(" gelen resim valid......")
            kaydet = form.save(commit=False)
            #kaydet.foto_kucuk = request.FILES.get('form_data')
            print(" kaydet foto küçük...", kaydet.foto_kucuk)
            if bool(kaydet.foto_kucuk):
                print("küçük resim dolu..............")
            else:
                print("küçük resim boş................")
            kaydet.save()
            print("kaydetmiş olması lazım.................")

            #buraya ekleme yapıldı , yazılan küçük resim dosyasını sonuc_resme de kaydedecek, belki silecek ???...
            sonuc_detay_id = request.session.get('sonuc_detay_id')
            print("İŞTE SONUÇ DETAY ID...", sonuc_detay_id)
            uploaded_image_obj = kucukresim.objects.filter(kullanici=request.user.id).last()
            print(" upload image object", uploaded_image_obj)
            uploaded_image = uploaded_image_obj.foto_kucuk
            #edit.foto = file(uploaded_image, os.path.basename(uploaded_image.path))
            print("yollu.........",  os.path.basename(uploaded_image.path))
            print("ikinci yollu...", os.path.abspath(uploaded_image.path))
            str1 = os.path.abspath(uploaded_image.path)
            str2 = "/home/levent/nata/media_cdn/"
            if str2 in str1:
                print("içinde....")
                str1 = str1.replace(str2,'')
            print("sonuç.........", str1)
            #edit.foto = os.path.abspath(uploaded_image.path)

            kaydetme_obj = sonuc_resim(sonuc_detay_id=sonuc_detay_id, foto=str1)
            kaydetme_obj.save()
            sonuc_detay_obj = sonuc_detay.objects.get(id=sonuc_detay_id)
            denetim_no = sonuc_detay_obj.denetim.id
        else:
            print("bu ibnenin nesi valid değil anlamadım ki......")
    print ("son nokta  küçük resim al....", response_data)
    #return HttpResponse(response_data, content_type='application/json')
    return HttpResponseRedirect(reverse('sonuc_denetim_detay_duzenle', args=(denetim_no, sonuc_detay_id,)))



@login_required
@csrf_exempt
def kucuk_resim_sil(request, pk_den=None, pk=None):
    print("selam buraya geldik.... küçük resim sil...")
    response_data ={}
    if request.method == 'POST':
        js_id = request.POST.get('id_verisi')
        sonuc_detay_id = request.session.get('sonuc_detay_id')
        print("silinecek kaydın id si...", js_id)
        print("ana sonuç detay...", sonuc_detay_id)
        silme_obj = sonuc_resim.objects.filter(id=js_id)
        if silme_obj:
            silme_obj.delete()
        else:
            print("silinecek kayıt bulunamadı......")
    print ("son nokta  küçük resim sil....", response_data)
    return HttpResponse(response_data, content_type='application/json')
    #return HttpResponseRedirect(reverse('sonuc_denetim_detay_duzenle', args=(sonuc_detay_id,)))






#--------------------------------------------------------------------------------


@login_required
def qrcode_tara(request, pk=None):

        context = {}
        return render(request, 'islem/qrcode_islemleri.html', context )




#--------------------------------------------------------------------------------


@login_required
def qrcode_calistir_js(request, pk=None):
    print("selam buraya geldik...qrcode çalıştır js")
    print("User.id.....:", request.user.id)
    #kullanan = request.user.id
    response_data ={}
    if request.method == 'GET':
        js_qrcode_result = request.GET.get('result')
        request.session['js_qrcode_result'] = js_qrcode_result
        print("  js içinden  okunan değer....",  js_qrcode_result)
    print ("son nokta denetim bölüm js.....", response_data)
    return HttpResponse(response_data, content_type='application/json')


#--------------------------------------------------------------------------------


@login_required
def nfc_oku(request, pk=None):
    print("selam buraya geldik...nfc_oku")
    nfc_degeri = pk
    print("nfc değeri...", nfc_degeri)
    request.session['js_qrcode_result'] = nfc_degeri
    return redirect('qrcode_islemi_baslat')



#--------------------------------------------------------------------------------


@login_required
def qrcode_islemi_baslat(request, pk=None):
    print("selam buraya geldik...qrcode islemi baslat")
    result = request.session.get('js_qrcode_result')
    print(" qrcode işlemi başlat içinden okunan değer....",  result)

    if result == None:
        messages.success(request, 'Code okunamadı')
        return redirect('qrcode_tara')

    result2 = str(result)
    print("result2....str olmuş ise", result2)
    newstr = result2[-4:]
    print("new string....", newstr)

    qr_obj = qrdosyasi.objects.filter(qr_deger=newstr).first()

    print("qr_obj... qrcode işlem başlat içinden...", qr_obj)

    if qr_obj:
        denetim = qr_obj.denetim
        request.session['rutin_secili_denetim'] = denetim.id
        print(" qrcode başlat içinden  denetim no", denetim.id)
        return redirect('rutin_baslat_kesin')
    else:
        messages.success(request, 'Code eşleşmedi')
        return redirect('qrcode_tara')

    context = {'result' : result}
    return render(request, 'islem/qrcode_islemleri_deneme.html', context )



#--------------------------------------------------------------------------------


@login_required
def cagir1(request, pk=None):
    print("selam buraya geldik...cagir1")
    context = {}
    return render(request, 'islem/ug_login.html', context )



@login_required
def cagir2(request, pk=None):
    print("selam buraya geldik...cagir1")
    context = {}
    return render(request, 'islem/ug_index.html', context )



@login_required
def cagir3(request, pk=None):
    print("selam buraya geldik...cagir1")
    context = {}
    return render(request, 'islem/ug_denetim.html', context )


@login_required
def cagir4(request, pk=None):
    print("selam buraya geldik...cagir1")
    context = {}
    return render(request, 'islem/ug_olustur.html', context )







#--------------------------------------------------------------------------------


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# işemri sonrası denetim seçimi ile ilgili bölüm.....
# önce denetim seçiliyor...

@login_required
def isemrisonrasi_sec(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = IlkDenetimSecForm(request.POST, kullanan=kullanan, durum="A")
        print("denetimi seçti gözlemci seçimi için...")
        # check whether it's valid:            denetim_obj.hedef_baslangic = yeni_baslangic

        if form.is_valid():
            print("valid....")
            denetim_no = request.POST.get('denetim_no', "")
            print ("denetim_no", denetim_no)
            request.session['ilk_secili_denetim'] = denetim_no
            #form = GozlemciForm()
            return redirect('isemrisonrasi_devam')
            #return render(request, 'islem/gozlemci_sec_devam.html', {'form': form,})
        else:
            print(" nah valid............")
            return render(request, 'islem/isemrisonrasi_denetim_sec.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        #ilk_secili_denetim = request.session.get('ilk_secili_denetim')
        kullanan = request.user.id
        print("kullanan  ..", kullanan)
        form = IlkDenetimSecForm(kullanan=kullanan, durum="B")
        return render(request, 'islem/isemrisonrasi_denetim_sec.html', {'form': form,})

#-------------------------------------------------------------------------------

@login_required
def isemrisonrasi_devam(request, pk=None):
    denetim_no = request.session.get('ilk_secili_denetim')
    print("iş emri sonrası devam....seçili denetim...", denetim_no)
    #gozlemci = ""
    bol_varmi = sonuc_bolum.objects.filter(denetim=denetim_no)
    print("bölümler", bol_varmi)
    det_varmi = sonuc_detay.objects.filter(denetim=denetim_no)
    print("detaylar", det_varmi)
    tak_varmi = sonuc_takipci.objects.filter(denetim=denetim_no)
    print("takipciler", tak_varmi)

    if not(tak_varmi):
        messages.success(request, 'Takipçi girilmemiş')
        return redirect('isemri_denetim_sec')
    if not(bol_varmi):
        messages.success(request, 'Bölümler girilmemiş')
        return redirect('isemri_denetim_sec')
    if not(det_varmi):
        messages.success(request, 'Detaylar girilmemiş')
        return redirect('isemri_denetim_sec')

    denetim_obj = denetim.objects.get(id=denetim_no)
    print("seçilen denetim", denetim_obj)
    denetim_obj.hedef_baslangic = yeni_baslangic
    denetim_adi = denetim_obj.denetim_adi
    proje = denetim_obj.proje
    rutin_planli = denetim_obj.rutin_planli
    denetci = denetim_obj.denetci
    tipi = denetim_obj.tipi
    yaratim_tarihi = denetim_obj.yaratim_tarihi
    yaratan = denetim_obj.yaratan
    hedef_baslangic = denetim_obj.hedef_baslangicsecili_musteri = request.session.get('secili_musteri')
    hedef_bitis = denetim_obj.hedef_bitis
    gerc_baslangic = denetim_obj.gerc_baslangic
    gerc_bitis = denetim_obj.gerc_bitis
    durum = denetim_obj.durum
    # gözlemci listesi...............................
    takipci_obj = sonuc_takipci.objects.filter(denetim=denetim_no)
    i = 0
    takipciler = []
    for takipci in takipci_obj:
        takipciler.append(takipci.takipci)
        i = i + 1
    print("takipciler list...",takipciler)
    # bölüm ve detay listesi..........................
    d = collections.defaultdict(list)
    bolum_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
    for bolum in bolum_obj:
        print("bolum list . bolum", bolum.bolum)
        detay_obj = sonuc_detay.objects.filter(denetim=denetim_no, bolum=bolum.bolum)
        for detay in detay_obj:
            print("detay list . detay", detay.bolum, detay.detay)
            d[detay.bolum].append(detay.detay)
    print("***********************")
    print(d)
    d.default_factory = None
    dict_bol_detay = dict(d)
    print("************************")
    print(dict_bol_detay)
    print(takipciler)
    context = {'dict_bol_detay':dict_bol_detay,
               'takipciler': takipciler,
               'denetim_adi': denetim_adi,
               'proje' : proje,
               'rutin_planli' : rutin_planli,
               'denetci' : denetci,
               'tipi' : tipi,
               'yaratim_tarihi' : yaratim_tarihi,
               'yaratan' : yaratan,
               'hedef_baslangic' : hedef_baslangic,
               'hedef_bitis' : hedef_bitis,
               'durum' : durum,
               }
    return render(request, 'islem/isemrisonrasi_sec_devam.html', context )




#------------------------------------------------------------------------------
# başlamnış ama bitirilmemiş denetim seçimi ile ilgili bölüm.....
# önce denetim seçiliyor...

@login_required
def baslanmislar_sec(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = IlkDenetimSecForm(request.POST, kullanan=kullanan, durum="B")
        print("denetimi seçti gözlemci seçimi için...")
        # check whether it's valid:

        if form.is_valid():
            print("valid....")
            denetim_no = request.POST.get('denetim_no', "")
            print ("denetim_no", denetim_no)
            request.session['ilk_secili_denetim'] = denetim_no
            #form = GozlemciForm()
            return redirect('baslanmislar_devam')
            #return render(request, 'islem/gozlemci_sec_devam.html', {'form': form,})
        else:
            print(" nah valid............")
            return render(request, 'islem/baslanmislar_denetim_sec.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        #ilk_secili_denetim = request.session.get('ilk_secili_denetim')
        kullanan = request.user.id
        print("kullanan  ..", kullanan)
        form = IlkDenetimSecForm(kullanan=kullanan, durum="B")
        return render(request, 'islem/baslanmislar_denetim_sec.html', {'form': form,})

#-------------------------------------------------------------------------------

@login_required
def baslanmislar_devam(request, pk=None):
    denetim_no = request.session.get('ilk_secili_denetim')
    print("iş emri sonrası devam....seçili denetim...", denetim_no)
    #gozlemci = ""
    bol_varmi = sonuc_bolum.objects.filter(denetim=denetim_no)
    print("bölümler", bol_varmi)
    det_varmi = sonuc_detay.objects.filter(denetim=denetim_no)
    print("detaylar", det_varmi)
    tak_varmi = sonuc_takipci.objects.filter(denetim=denetim_no)
    print("takipçiler", tak_varmi)

    if not(tak_varmi):
        messages.success(request, 'Takipçi girilmemiş')
        return redirect('isemri_denetim_sec')
    if not(bol_varmi):
        messages.success(request, 'Bölümler girilmemiş')
        return redirect('isemri_denetim_sec')
    if not(det_varmi):
        messages.success(request, 'Detaylar girilmemiş')
        return redirect('isemri_denetim_sec')

    denetim_obj = denetim.objects.get(id=denetim_no)
    print("seçilen denetim", denetim_obj)
    denetim_adi = denetim_obj.denetim_adi
    proje = denetim_obj.proje
    rutin_planli = denetim_obj.rutin_planli
    denetci = denetim_obj.denetci
    tipi = denetim_obj.tipi
    yaratim_tarihi = denetim_obj.yaratim_tarihi
    yaratan = denetim_obj.yaratan
    hedef_baslangic = denetim_obj.hedef_baslangic
    hedef_bitis = denetim_obj.hedef_bitis
    gerc_baslangic = denetim_obj.gerc_baslangic
    gerc_bitis = denetim_obj.gerc_bitis
    durum = denetim_obj.durum
    # gözlemci listesi...............................
    takipci_obj = sonuc_takipci.objects.filter(denetim=denetim_no)
    i = 0
    takipciler = []
    for takipci in takipci_obj:
        takipciler.append(takipci.takipci)
        i = i + 1
    print("takipciler list...",takipciler)
    # bölüm ve detay listesi..........................
    d = collections.defaultdict(list)
    bolum_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
    for bolum in bolum_obj:
        print("bolum list . bolum", bolum.bolum)
        detay_obj = sonuc_detay.objects.filter(denetim=denetim_no, bolum=bolum.bolum)
        for detay in detay_obj:
            print("detay list . detay", detay.bolum, detay.detay)
            d[detay.bolum].append(detay.detay)
    print("***********************")
    print(d)
    d.default_factory = None
    dict_bol_detay = dict(d)
    #gozgoz = takipciler
    print("************************")
    print(dict_bol_detay)
    print(takipciler)
    context = {'dict_bol_detay':dict_bol_detay,
               'takipciler': takipciler,
               'denetim_adi': denetim_adi,
               'proje' : proje,
               'rutin_planli' : rutin_planli,
               'denetci' : denetci,
               'tipi' : tipi,
               'yaratim_tarihi' : yaratim_tarihi,
               'yaratan' : yaratan,
               'hedef_baslangic' : hedef_baslangic,
               'hedef_bitis' : hedef_bitis,
               'durum' : durum,
               }
    return render(request, 'islem/baslanmislar_sec_devam.html', context )



#------------------------------------------------------------------------------
# sonlandırılan denetim seçimi ile ilgili bölüm.....
# önce denetim seçiliyor...

@login_required
def sonlandirilan_sec(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = ProjeSecForm(request.POST)
        print("denetimi seçti gözlemci seçimi için...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            proje = request.POST.get('proje', "")
            print ("proje", proje)
            request.session['secili_proje'] = proje
            #form = GozlemciForm()
            return redirect('sonlandirilan_devam')
            #return render(request, 'islem/gozlemci_sec_devam.html', {'form': form,})
        else:
            print(" nah valid............")
            return render(request, 'islem/sonlandirilan_proje_sec.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        #ilk_secili_denetim = request.session.get('ilk_secili_denetim')
        kullanan = request.user.id
        print("kullanan  ..", kullanan)
        form = ProjeSecForm()
        return render(request, 'islem/sonlandirilan_proje_sec.html', {'form': form,})

#-------------------------------------------------------------------------------

@login_required
def sonlandirilan_devam(request, pk=None):
    secili_proje = request.session.get('secili_proje')
    #musteri_no = int(secili_musteri)
    #print("seçili musteri...", secili_musteri, "musteri no..:", musteri_no)
    proje_obj = proje.objects.get(id=secili_proje)
    #sonlandirilan_denetim_obj = denetim.objects.filter(musteri=secili_musteri).filter(durum="D")
    sonlandirilan_denetim_obj = denetim.objects.filter(proje=secili_proje)
    context = {'sonlandirilan_denetim_obj':sonlandirilan_denetim_obj,
               'proje_obj': proje_obj,
               }
    return render(request, 'islem/sonlandirilan_denetim_list.html', context )


#-------------------------------------------------------------------------------

@login_required
def sonlandirilan_ilerle(request, pk=None):
    denetim_no = pk
    request.session['secilen_denetim'] = denetim_no
    sonuc_list = sonuc_detay.objects.filter(denetim=denetim_no).order_by('bolum')
    denetimin_adi = sonuc_list.first().denetim.denetim_adi
    denetimin_durumu = sonuc_list.first().denetim.durum
    context = {'sonuc_list': sonuc_list, 'denetimin_adi': denetimin_adi, 'denetimin_durumu': denetimin_durumu}
    return render(request, 'islem/sonlandirilan_detay_list.html', context)




#------------------------------------------------------------------------------
# sonlandırılan denetim seçimi ile ilgili bölüm.....
# önce denetim seçiliyor...






@login_required
def raporlar_sec(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = ProjeSecForm(request.POST)
        print("denetimi seçti gözlemci seçimi için...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            proje = request.POST.get('proje', "")
            print ("proje", proje)
            request.session['secili_proje'] = proje
            return redirect('raporlar_devam')
            #return render(request, 'islem/gozlemci_sec_devam.html', {'form': form,})
        else:
            print(" nah valid............")
            return render(request, 'islem/raporlar_proje_sec.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        #ilk_secili_denetim = request.session.get('ilk_secili_denetim')
        kullanan = request.user.id
        print("kullanan  ..", kullanan)
        form = ProjeSecForm()
        return render(request, 'islem/raporlar_proje_sec.html', {'form': form,})

#-------------------------------------------------------------------------------

@login_required
def raporlar_devam(request, pk=None):
    secili_proje = request.session.get('secili_proje')
    #musteri_no = int(secili_musteri)
    #print("seçili musteri...", secili_musteri, "musteri no..:", musteri_no)
    proje_obj = proje.objects.get(id=secili_proje)
    #sonlandirilan_denetim_obj = denetim.objects.filter(musteri=secili_musteri).filter(durum="D")
    raporlar_denetim_obj = denetim.objects.filter(proje=secili_proje).filter(durum="C")
    context = {'raporlar_denetim_obj':raporlar_denetim_obj,
               'proje_obj': proje_obj,
               }
    return render(request, 'islem/raporlar_denetim_list.html', context )



#-------------------------------------------------------------------------------

@login_required
def raporlar_ilerle(request, pk=None):
    denetim_no = pk

    if rapor_verisi_hazirla(request, denetim_no=denetim_no):
        denetim_obj = denetim.objects.get(id=denetim_no)
        denetim_adi = denetim_obj.denetim_adi
        proje = denetim_obj.proje
        rutin_planli = denetim_obj.rutin_planli
        denetci = denetim_obj.denetci
        tipi = denetim_obj.tipi
        yaratim_tarihi = denetim_obj.yaratim_tarihi
        yaratan = denetim_obj.yaratan
        hedef_baslangic = denetim_obj.hedef_baslangic
        hedef_bitis = denetim_obj.hedef_bitis
        gerc_baslangic = denetim_obj.gerc_baslangic
        gerc_bitis = denetim_obj.gerc_bitis
        durum = denetim_obj.durum
        rutindenetci = denetim_obj.rutindenetci
        takipci_obj = sonuc_takipci.objects.filter(denetim=denetim_no)
        print("takipci objesi...", takipci_obj)
        i = 0
        takipciler = []
        for takipci in takipci_obj:
            takipciler.append(takipci.takipci)
            i = i + 1
        print("takipciler listesi..", takipciler)
        d = collections.defaultdict(list)
        bolum_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
        for bolum in bolum_obj:
            print("bolum list . bolum", bolum.bolum)
            detay_obj = sonuc_detay.objects.filter(denetim=denetim_no, bolum=bolum.bolum).order_by('detay')
            for detay in detay_obj:
                print("detay list . detay", detay.bolum, detay.detay)
                #d[detay.bolum].append(detay.detay)
                d[bolum].append(detay)
        print("***********************")
        print(d)
        d.default_factory = None
        dict_bol_detay = dict(d)
        print("************************")
        print(dict_bol_detay)
        context = { 'dict_bol_detay':dict_bol_detay,
                    'takipciler': takipciler,
                    'denetim_adi': denetim_adi,
                    'proje' : proje,
                    'rutin_planli' : rutin_planli,
                    'rutindenetci' : rutindenetci,
                    'denetci' : denetci,
                    'tipi' : tipi,
                    'yaratim_tarihi' : yaratim_tarihi,
                    'yaratan' : yaratan,
                    'hedef_baslangic' : hedef_baslangic,
                    'hedef_bitis' : hedef_bitis,
                    'durum' : durum,
                    'soru_adedi' : denetim_soru,
                    'dd_adedi' :  denetim_dd,
                    'net_adet' : denetim_net,
                    'toplam_puan' : denetim_puan,
                    'ortalama_puan' : ortalama_puan,
                    'pk' : denetim_no,
                    }
        #return render(request, 'islem/teksayfa_sil_soru.html', context )
        return render(request, 'islem/denetim_rapor_goster.html', context )

    else:
        mesaj = request.session.get('mesaj_rapor_verisi')
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})



#------------------------------------------------------------------------------
# sonlandırılan denetim seçimi ile ilgili bölüm.....
# önce denetim seçiliyor...

@login_required
def rapor_yazisi(request, pk=None):
    # if this is a POST request we need to process the form data
    kullanan = request.user
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = YaziForm(request.POST, kullanan=kullanan)
        print("denetimi seçti gözlemci seçimi için...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            denetim_no = request.POST.get('denetim', "")
            yazi = request.POST.get('yazi',"")
            print ("denetim", denetim_no)
            print ("yazi", yazi)
            kaydetme_obj = denetim.objects.get(id=denetim_no)
            kaydetme_obj.rapor_yazi = yazi
            kaydetme_obj.yazi_varmi = "E"
            kaydetme_obj.save()
            return redirect('index')
        else:
            print(" valid değil rapor yazisi ...........")
            return render(request, 'islem/rapor_yazisi.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        #ilk_secili_denetim = request.session.get('ilk_secili_denetim')
        form = YaziForm(kullanan=kullanan)
        return render(request, 'islem/rapor_yazisi.html', {'form': form,})


#------------------------------------------------------------------------------
# sonlandırılan denetim seçimi ile ilgili bölüm.....
# önce denetim seçiliyor...


@login_required
@csrf_exempt
def rapor_yazisi_al(request):
    print("selam buraya geldik.... rapor yazisi al...")
    response_data ={}
    if request.method == 'POST':
        js_denetim = request.POST.get('denetim')
        print("js_denetim...", js_denetim)
        denetim_obj = denetim.objects.get(id=js_denetim)
        print("denetim obj", denetim_obj)
        data = denetim_obj.rapor_yazi
        print("gönderilecek data", data)
        response_data = {'data': data}
    print ("son nokta  rapor yazisi al....", response_data)
    return HttpResponse(json.dumps(data), content_type='application/json')
    #return HttpResponse(data, content_type='application/json')




#------------------------------------------------------------------------------
# sonlandırılan denetim seçimi ile ilgili bölüm.....
# önce denetim seçiliyor...

@login_required
def iptal_sec(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = ProjeSecForm(request.POST)
        print("denetimi seçti gözlemci seçimi için...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            proje = request.POST.get('proje', "")
            print ("proje", proje)
            request.session['secili_proje'] = proje
            #form = GozlemciForm()
            return redirect('iptal_devam')
            #return render(request, 'islem/gozlemci_sec_devam.html', {'form': form,})
        else:
            print(" nah valid............")
            return render(request, 'islem/iptal_proje_sec.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        #ilk_secili_denetim = request.session.get('ilk_secili_denetim')
        kullanan = request.user.id
        print("kullanan  ..", kullanan)
        form = ProjeSecForm()
        return render(request, 'islem/iptal_proje_sec.html', {'form': form,})

#-------------------------------------------------------------------------------

@login_required
def iptal_devam(request, pk=None):
    secili_proje = request.session.get('secili_proje')
    proje_obj = proje.objects.get(id=secili_proje)
    iptal_denetim_obj = denetim.objects.filter(proje=secili_proje).filter(durum="C")
    context = {'iptal_denetim_obj': iptal_denetim_obj,
               'proje_obj': proje_obj,
               }
    return render(request, 'islem/iptal_denetim_list.html', context )


#-------------------------------------------------------------------------------

@login_required
def iptal_ilerle(request, pk=None):
    denetim_no = pk
    request.session['ilk_secili_denetim'] = denetim_no

    denetim_obj = denetim.objects.get(id=denetim_no)

    bolumler_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
    if not(bolumler_obj):
        mesaj = "Denetime ait bölüm yok!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})

    kontrol_degiskeni = True
    for bolum in bolumler_obj:
        if bolum.tamam == "H":
            kontrol_degiskeni = False

    if not(kontrol_degiskeni):
        mesaj = "Tamamlanmamış bölümler var!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})


    #########################################################################
    ###   RAPOR
    #########################################################################
    if not(rapor_verisi_hazirla(request, denetim_no=pk)):
        mesaj = "Rapor verisi hazırlanamadı..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    else:
        denetim_adi = denetim_obj.denetim_adi
        proje = denetim_obj.proje
        rutin_planli = denetim_obj.rutin_planli
        denetci = denetim_obj.denetci
        tipi = denetim_obj.tipi
        yaratim_tarihi = denetim_obj.yaratim_tarihi
        yaratan = denetim_obj.yaratan
        hedef_baslangic = denetim_obj.hedef_baslangic
        hedef_bitis = denetim_obj.hedef_bitis
        gerc_baslangic = denetim_obj.gerc_baslangic
        gerc_bitis = denetim_obj.gerc_bitis
        durum = denetim_obj.durum
        rutindenetci = denetim_obj.rutindenetci
        takipci_obj = sonuc_takipci.objects.filter(denetim=denetim_no)
        print("takipci objesi...", takipci_obj)
        i = 0
        takipciler = []
        for takipci in takipci_obj:
            takipciler.append(takipci.takipci)
            i = i + 1
        print("takipciler listesi..", takipciler)
        d = collections.defaultdict(list)
        bolum_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
        for bolum in bolum_obj:
            print("bolum list . bolum", bolum.bolum)
            detay_obj = sonuc_detay.objects.filter(denetim=denetim_no, bolum=bolum.bolum).order_by('detay')
            for detay in detay_obj:
                print("detay list . detay", detay.bolum, detay.detay)
                #d[detay.bolum].append(detay.detay)
                d[bolum].append(detay)
        print("***********************")
        print(d)
        d.default_factory = None
        dict_bol_detay = dict(d)
        print("************************")
        print(dict_bol_detay)
        context = {'dict_bol_detay':dict_bol_detay,
                    'takipciler': takipciler,
                    'denetim_adi': denetim_adi,
                    'proje' : proje,
                    'rutin_planli' : rutin_planli,
                    'rutindenetci' : rutindenetci,
                    'denetci' : denetci,
                    'tipi' : tipi,
                    'yaratim_tarihi' : yaratim_tarihi,
                    'yaratan' : yaratan,
                    'hedef_baslangic' : hedef_baslangic,
                    'hedef_bitis' : hedef_bitis,
                    'durum' : durum,
                    'soru_adedi' : denetim_soru,
                    'dd_adedi' :  denetim_dd,
                    'net_adet' : denetim_net,
                    'toplam_puan' : denetim_puan,
                    'ortalama_puan' : ortalama_puan,
                    'pk' : denetim_no,
                    }
        #return render(request, 'islem/teksayfa_sil_soru.html', context )
        #return render(request, 'islem/denetim_rapor_goster.html', context )

        return render(request, 'islem/denetim_iptal_sor.html', context )



#------------------------------------------------------------------
#  denetimi tamamlama işlemleri önce sor sonra tamamla

@login_required
def denetim_iptal(request, pk=None):

    denetim_no = request.session.get('ilk_secili_denetim')
    denetim_obj = denetim.objects.get(id=denetim_no)
    print("seçilen denetim", denetim_obj)
    numarasi = denetim_obj.id
    denetim_adi = denetim_obj.denetim_adi
    context = {'denetim_adi': denetim_adi,
               'numarasi' : numarasi,
              }
    return render(request, 'islem/denetim_iptal_sor.html', context )


#--------------------------------------------------------------------------------

# denetim iptal ediliyor Y yapılıyor....

@login_required
def denetim_iptal_devam(request, pk=None):

    denetim_no = request.session.get('ilk_secili_denetim')
    denetim_obj = denetim.objects.get(id=denetim_no)
    print("seçilen denetim kesin ...", denetim_obj)
    denetim_obj.durum = "Y"
    denetim_obj.save()
    messages.success(request, 'Denetim iptal edildi')
    return redirect('index' )


#--------------------------------------------------------------------------------

@login_required
def soru_listesi(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SoruListesiForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            tipi_i = request.POST.get('tipi', "")
            zon_i = request.POST.get('zon', "")
            bolum_i = request.POST.get('bolum', "")
            print ("tipi....", tipi_i)
            print("zon...", zon_i)
            print("bölüm..", bolum_i)
            request.session['sorulist_tipi'] = tipi_i
            request.session['sorulist_zon'] = zon_i
            request.session['sorulist_bolum'] = bolum_i

            return redirect('/islem/soru_listesi/devam/')

        else:
            messages.success(request, 'Formda uygunsuzluk var')
            #return redirect('soru_listesi')
            return render(request, 'islem/soru_listesi.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        #selected_alt = request.session.get('selected_alt')
        form = SoruListesiForm()
        return render(request, 'islem/soru_listesi.html', {'form': form,})


@login_required
def soru_listesi_devam(request, pk=None):
    # if this is a POST request we need to process the form data
    tipi_i = request.session.get('sorulist_tipi')
    zon_i = request.session.get('sorulist_zon')
    bolum_i = request.session.get('sorulist_bolum')
    request.session['sorulist_kopyala_tipi'] = None
    request.session['sorulist_kopyala_zon'] = None
    request.session['sorulist_kopyala_bolum'] = None
    #request.session['sorulist_kopyala_sorulist'] = None
    request.session['sorulist_kopyala_flag'] = False
    print ("tipi....", tipi_i)
    print("zon...", zon_i)
    print("bölüm..", bolum_i)
    tipi_l = tipi.objects.get(id=tipi_i)
    zon_l = zon.objects.get(id=zon_i)
    bolum_l = bolum.objects.get(id=bolum_i)
    soru_list = detay.objects.filter(bolum=bolum_i)
    context = {'tipi': tipi_l,
               'zon' : zon_l,
               'bolum' : bolum_l,
               'soru_list' : soru_list,
              }
    return render(request, 'islem/soru_listesi_devam.html', context )


@login_required
def soru_listesi_yarat(request, pk=None):
    # if this is a POST request we need to process the form data
    bolum = request.session.get('sorulist_bolum')
    print("soru listesi yarat içinden bölüm...", bolum)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = SoruForm(request.POST)
        print("soruform okundu...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            detay_kodu = request.POST.get('detay_kodu', "")
            detay_adi = request.POST.get('detay_adi', "")
            puanlama_turu = request.POST.get('puanlama_turu', "")
            kaydetme_obj = detay(detay_kodu=detay_kodu,
                                 detay_adi=detay_adi,
                                 bolum_id=bolum,
                                 puanlama_turu=puanlama_turu)
            kaydetme_obj.save()
            return redirect('soru_listesi_devam')
        else:
            print(" not valid............")
            return render(request, 'islem/soru_listesi.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = SoruForm()
        return render(request, 'islem/soru_form.html', {'form': form,})


@login_required
def soru_listesi_duzenle(request, pk=None):
    # if this is a POST request we need to process the form data
    bolum = request.session.get('sorulist_bolum')
    print("soru listesi düzenle içinden bölüm...", bolum)
    detay_obj = detay.objects.get(id=pk)
    print("soru listesi düzenle içinden detay obj..", detay_obj)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = SoruForm(request.POST)
        print("soruform okundu...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            detay_kodu = request.POST.get('detay_kodu', "")
            detay_adi = request.POST.get('detay_adi', "")
            puanlama_turu = request.POST.get('puanlama_turu', "")
            kaydetme_obj = detay(id=pk,
                                 detay_kodu=detay_kodu,
                                 detay_adi=detay_adi,
                                 bolum_id=bolum,
                                 puanlama_turu=puanlama_turu)
            kaydetme_obj.save()
            return redirect('soru_listesi_devam')
        else:
            print(" not valid............")
            return render(request, 'islem/soru_listesi.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = SoruForm()
        form.fields["detay_kodu"].initial = detay_obj.detay_kodu
        form.fields["detay_adi"].initial = detay_obj.detay_adi
        form.fields["puanlama_turu"].initial = detay_obj.puanlama_turu
        return render(request, 'islem/soru_form.html', {'form': form,})


@login_required
def soru_listesi_sil(request, pk=None):
    # if this is a POST request we need to process the form data
    soru_obj = detay.objects.get(id=pk)
    print("soru listesi sil içinden detay obj..", soru_obj)
    context = {'soru' : soru_obj,
              }
    return render(request, 'islem/soru_sil_soru.html', context )



@login_required
def soru_listesi_sil_kesin(request, pk=None):
    object = get_object_or_404(detay, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    messages.success(request, 'Başarıyla silindi')
    return redirect('soru_listesi_devam')



@login_required
def soru_listesi_kopyala(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SoruListesiForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            tipi_i = request.POST.get('tipi', "")
            zon_i = request.POST.get('zon', "")
            bolum_i = request.POST.get('bolum', "")
            print ("tipi....", tipi_i)
            print("zon...", zon_i)
            print("bölüm..", bolum_i)
            request.session['sorulist_kopyala_tipi'] = tipi_i
            request.session['sorulist_kopyala_zon'] = zon_i
            request.session['sorulist_kopyala_bolum'] = bolum_i

            return redirect('/islem/soru_listesi/devam/kopyala/kesin/')

        else:
            messages.success(request, 'Formda uygunsuzluk var')
            return redirect('soru_listesi')
            #return render(request, 'islem/denetim_deneme_form.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        #selected_alt = request.session.get('selected_alt')
        print("soru aktarım ilk get bölümü..,  soru listesi kopyala...")
        tipi_i = request.session.get('sorulist_kopyala_tipi')
        zon_i = request.session.get('sorulist_kopyala_zon')
        bolum_i =  request.session.get('sorulist_kopyala_bolum')
        print("tipi", tipi_i)
        print("zon", zon_i)
        print("bolum", bolum_i)
        soru_list = detay.objects.filter(bolum=bolum_i)
        kopya_flag = request.session.get('sorulist_kopyala_flag')
        form = SoruListesiForm()
        form.fields["tipi"].initial = tipi_i
        form.fields["zon"].initial = zon_i
        form.fields["bolum"].initial = bolum_i
        return render(request, 'islem/soru_kopyala.html', {'form': form, 'soru_list': soru_list, 'kopya_flag': kopya_flag})

@login_required
def soru_kopyala_js(request, pk=None):
    print("selam buraya geldik...soru kopyala js")
    kullanan = request.user.id
    response_data ={}
    if request.method == 'GET':
        js_tipi = request.GET.getlist('js_tipi')
        js_zon = request.GET.get('js_zon')
        js_bolum = request.GET.get('js_bolum')
        print("tipi-zon-bolum..", js_tipi, js_zon, js_bolum)
        request.session['sorulist_kopyala_tipi'] = js_tipi
        request.session['sorulist_kopyala_zon'] = js_zon
        request.session['sorulist_kopyala_bolum'] = js_bolum
        #detay_obj = detay.objects.filter(bolum=js_bolum)
        kopya_flag = True
        #request.session['sorulist_kopyala_sorulist'] = detay_obj
        request.session['sorulist_kopyala_flag'] = kopya_flag
        #response_data = {'soru_list': detay_obj, 'kopya_flag': kopya_flag}
    print ("son nokta soru kopyala js.....", response_data)
    return HttpResponse(response_data, content_type='application/json')



@login_required
@transaction.atomic
def soru_listesi_kopyala_kesin(request, pk=None):
    bolum_yaz = request.session.get('sorulist_kopyala_bolum')
    bolum_ver = request.session.get('sorulist_bolum')
    print("soruların yazılacağı bolum..", bolum_yaz)
    print("soruların alınacağı bölüm", bolum_ver)
    any_obj = detay.objects.filter(bolum=bolum_yaz)
    print("soru listesi kopyala kesin içinden detay obj..", any_obj)
    if any_obj:
        for any_detay in any_obj:
            kaydetme_obj=detay( id=any_detay.id,
                                #detay_kodu=any_detay.detay_kodu,
                                #detay_adi=any_detay.detay_adi,
                                #bolum_id=any_detay.bolum,
                                #puanlama_turu=any_detay.puanlama_turu,
                                sil=True)
            kaydetme_obj.save()
    yeni_detay_obj = detay.objects.filter(bolum=bolum_ver)
    for detaylar in yeni_detay_obj:
        kaydetme_obj=detay(detay_kodu=detaylar.detay_kodu,
                            detay_adi=detaylar.detay_adi,
                            bolum_id=bolum_yaz,
                            puanlama_turu=detaylar.puanlama_turu)
        kaydetme_obj.save()
    messages.success(request, 'kopyalama işlemi gerçekleştirildi')
    return redirect('soru_listesi')




#--------------------------------------------------------------------------------

@login_required
def bolum_listesi(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BolumListesiForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            tipi_i = request.POST.get('tipi', "")
            zon_i = request.POST.get('zon', "")
            print ("tipi....", tipi_i)
            print("zon...", zon_i)
            request.session['bolumlist_tipi'] = tipi_i
            request.session['bolumlist_zon'] = zon_i

            return redirect('/islem/bolum_listesi/devam/')

        else:
            messages.success(request, 'Formda uygunsuzluk var')
            #return redirect('bolum_listesi')
            return render(request, 'islem/bolum_listesi.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        #selected_alt = request.session.get('selected_alt')
        form = BolumListesiForm()
        return render(request, 'islem/bolum_listesi.html', {'form': form,})


@login_required
def bolum_listesi_devam(request, pk=None):
    # if this is a POST request we need to process the form data
    tipi_i = request.session.get('bolumlist_tipi')
    zon_i = request.session.get('bolumlist_zon')
    print ("tipi....", tipi_i)
    print("zon...", zon_i)
    tipi_l = tipi.objects.get(id=tipi_i)
    zon_l = zon.objects.get(id=zon_i)
    bolum_list = bolum.objects.filter(zon=zon_l)
    context = {'tipi': tipi_l,
               'zon' : zon_l,
               'bolum_list' : bolum_list,
              }
    return render(request, 'islem/bolum_listesi_devam.html', context )


@login_required
def bolum_listesi_yarat(request, pk=None):
    # if this is a POST request we need to process the form data
    zon = request.session.get('bolumlist_zon')
    print("bölüm listesi yarat içinden zon", zon)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = BolumForm(request.POST)
        print("bölümform okundu...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            bolum_kodu = request.POST.get('bolum_kodu', "")
            bolum_adi = request.POST.get('bolum_adi', "")
            kaydetme_obj = bolum(bolum_kodu=bolum_kodu,
                                 bolum_adi=bolum_adi,
                                 zon_id=zon)
            kaydetme_obj.save()
            return redirect('bolum_listesi_devam')
        else:
            print(" geçerli değil............")
            return render(request, 'islem/bolum_listesi.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = BolumForm()
        return render(request, 'islem/bolum_form.html', {'form': form,})


@login_required
def bolum_listesi_duzenle(request, pk=None):
    # if this is a POST request we need to process the form data
    zon = request.session.get('bolumlist_zon')
    print("bölüm listesi düzenle içinden zon...", zon)
    bolum_obj = bolum.objects.get(id=pk)
    print("bölüm listesi düzenle içinden bölüm obj..", bolum_obj)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = BolumForm(request.POST)
        print("bölümform okundu...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            bolum_kodu = request.POST.get('bolum_kodu', "")
            bolum_adi = request.POST.get('bolum_adi', "")
            kaydetme_obj = bolum(id=pk,
                                 bolum_kodu=bolum_kodu,
                                 bolum_adi=bolum_adi,
                                 zon_id=zon)
            kaydetme_obj.save()
            return redirect('bolum_listesi_devam')
        else:
            print(" geçerli değil............")
            return render(request, 'islem/bolum_listesi.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = BolumForm()
        form.fields["bolum_kodu"].initial = bolum_obj.bolum_kodu
        form.fields["bolum_adi"].initial = bolum_obj.bolum_adi
        return render(request, 'islem/bolum_form.html', {'form': form,})


@login_required
def bolum_listesi_sil(request, pk=None):
    # if this is a POST request we need to process the form data
    bolum_obj = bolum.objects.get(id=pk)
    print("bölüm listesi sil içinden bölüm obj..", bolum_obj)
    context = {'bolum_obj' : bolum_obj,
              }
    return render(request, 'islem/bolum_sil_soru.html', context )



@login_required
def bolum_listesi_sil_kesin(request, pk=None):
    object = get_object_or_404(bolum, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    messages.success(request, 'Başarıyla silindi')
    return redirect('bolum_listesi_devam')


#------------------------------------------------------------------------------------

@login_required
def zon_listesi(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ZonListesiForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            tipi_i = request.POST.get('tipi', "")
            print ("tipi....", tipi_i)
            request.session['zonlist_tipi'] = tipi_i
            return redirect('/islem/zon_listesi/devam/')

        else:
            messages.success(request, 'Formda uygunsuzluk var')
            #return redirect('bolum_listesi')
            return render(request, 'islem/zon_listesi.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        #selected_alt = request.session.get('selected_alt')
        form = ZonListesiForm()
        return render(request, 'islem/zon_listesi.html', {'form': form,})


@login_required
def zon_listesi_devam(request, pk=None):
    # if this is a POST request we need to process the form data
    tipi_i = request.session.get('zonlist_tipi')
    print ("tipi....", tipi_i)
    tipi_l = tipi.objects.get(id=tipi_i)
    zon_list = zon.objects.filter(tipi=tipi_l)
    context = {'tipi': tipi_l,
               'zon_list' : zon_list,
              }
    return render(request, 'islem/zon_listesi_devam.html', context )


@login_required
def zon_listesi_yarat(request, pk=None):
    # if this is a POST request we need to process the form data
    tipi = request.session.get('zonlist_tipi')
    print("zon listesi yarat içinden tipi", tipi)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = ZonForm(request.POST)
        print("zonform okundu...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            zon_kodu = request.POST.get('zon_kodu', "")
            zon_adi = request.POST.get('zon_adi', "")
            kaydetme_obj = zon(zon_kodu=zon_kodu,
                                 zon_adi=zon_adi,
                                 tipi_id=tipi)
            kaydetme_obj.save()
            return redirect('zon_listesi_devam')
        else:
            print(" geçerli değil............")
            return render(request, 'islem/zon_listesi.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = ZonForm()
        return render(request, 'islem/zon_form.html', {'form': form,})


@login_required
def zon_listesi_duzenle(request, pk=None):
    # if this is a POST request we need to process the form data
    tipi = request.session.get('zonlist_tipi')
    print("zon listesi düzenle içinden tipi...", tipi)
    zon_obj = zon.objects.get(id=pk)
    print("zon listesi düzenle içinden zon obj..", zon_obj)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = ZonForm(request.POST)
        print("bölümform okundu...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            zon_kodu = request.POST.get('zon_kodu', "")
            zon_adi = request.POST.get('zon_adi', "")
            kaydetme_obj = zon(id=pk,
                                 zon_kodu=zon_kodu,
                                 zon_adi=zon_adi,
                                 tipi_id=tipi)
            kaydetme_obj.save()
            return redirect('zon_listesi_devam')
        else:
            print(" geçerli değil............")
            return render(request, 'islem/zon_listesi.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = ZonForm()
        form.fields["zon_kodu"].initial = zon_obj.zon_kodu
        form.fields["zon_adi"].initial = zon_obj.zon_adi
        return render(request, 'islem/zon_form.html', {'form': form,})


@login_required
def zon_listesi_sil(request, pk=None):
    # if this is a POST request we need to process the form data
    zon_obj = zon.objects.get(id=pk)
    print("zon listesi sil içinden zon obj..", zon_obj)
    context = {'zon_obj' : zon_obj,
              }
    return render(request, 'islem/zon_sil_soru.html', context )



@login_required
def zon_listesi_sil_kesin(request, pk=None):
    object = get_object_or_404(zon, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    messages.success(request, 'Başarıyla silindi')
    return redirect('zon_listesi_devam')




#------------------------------------------------------------------------------------

@login_required
def spv_listesi(request, pk=None):
    secili_sirket = request.user.profile.sirket
    print("işte kişinin şirketi...", secili_sirket)
    if not secili_sirket:
        mesaj = "kişinin bağlı olduğu şirket yok...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    spv_obj = spv_yetkilisi.objects.filter(sirket=secili_sirket)
    grup_list = []
    grupdisi_list = []

    for spv in spv_obj:
        kisi = spv.spv_yetkilisi.id
        kisi_obj = User.objects.get(id=kisi)
        print("kişi object...", kisi_obj)
        kisi_sirket = kisi_obj.profile.sirket
        print("kişi şirket..", kisi_sirket)
        if kisi_sirket:
            if kisi_sirket.turu == "P":
                grup_list.append(kisi_obj)
            else:
                grupdisi_list.append(kisi_obj)

    print("grup list..", grup_list)
    print("grup dışı list..", grupdisi_list)
    context = {'grup_list': grup_list, 'grupdisi_list': grupdisi_list}
    return render(request, 'islem/spv_list.html', context )



@login_required
def spv_yarat(request, pk=None):
    # if this is a POST request we need to process the form data
    kullanici = request.user
    sirket = kullanici.profile.sirket
    spvler_obj = Profile.objects.filter(denetim_grup_yetkilisi="E")

    serbest_spv_list = []
    for spv in spvler_obj:
        if spv.sirket.turu == "D":
            usr_obj = spv.user
            serbest_spv_list.append(usr_obj)
    print("serbest denetci...", serbest_spv_list)

    spv_obj = spv_yetkilisi.objects.filter(sirket=sirket)
    grupdisi_list = []
    for spv in spv_obj:
        kisi = spv.spv_yetkilisi.id
        kisi_obj = User.objects.get(id=kisi)
        print("kişi object...", kisi_obj)
        kisi_sirket = kisi_obj.profile.sirket
        print("kişi şirket..", kisi_sirket)
        if kisi_sirket:
            if kisi_sirket.turu == "D":
                grupdisi_list.append(kisi_obj)
    print("grup dışı list  dışarıdan şirkete atanmış olanlar.......", grupdisi_list)

    kalan_list = list(set(serbest_spv_list) - set(grupdisi_list))

    print("kontrolden sonra serbest denetci...", kalan_list)

    if not kalan_list:
        mesaj = "eklenecek süpervizör yok...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        #form = SpvForm(request.POST, serbest_spv=kalan_list)
        form = SpvForm(request.POST)
        print("spvform okundu...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            spv_yetkili = request.POST.getlist('spv', "")
            print("spv yetkili....", spv_yetkili)
            for x in spv_yetkili:
                kaydetme_obj = spv_yetkilisi(spv_yetkilisi_id=x, sirket_id=sirket.id)
                kaydetme_obj.save()
            return redirect('spv_listesi')
        else:
            print(" geçerli değil............")
            return render(request, 'islem/spv_form.html', {'form': form,})
    # if a GET (or any other method) we'll create a blank form
    else:

        #form = SpvForm(serbest_spv=kalan_list)
        form = SpvForm()
        return render(request, 'islem/spv_form.html', {'form': form,})




@login_required
def spv_listesi_sil(request, pk=None):
    # if this is a POST request we need to process the form data
    user_obj = User.objects.get(id=pk)
    kullanici = request.user
    sirket = kullanici.profile.sirket
    spv_obj = spv_yetkilisi.objects.filter(spv_yetkilisi=user_obj.id).filter(sirket=sirket)
    print("spv obj....", spv_obj)
    print("spv listesi sil içinden spv obj..", spv_obj)
    context = {'spv_obj' : spv_obj,
              }
    return render(request, 'islem/spv_sil_soru.html', context )



@login_required
def spv_listesi_sil_kesin(request, pk=None):
    user_obj = User.objects.get(id=pk)
    kullanici = request.user
    sirket = kullanici.profile.sirket
    spv_obj = spv_yetkilisi.objects.filter(spv_yetkilisi=user_obj.id).filter(sirket=sirket)
    #object = get_object_or_404(spv_yetkilisi, pk=pk)
    try:
        spv_obj.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    messages.success(request, 'Başarıyla silindi')
    return redirect('spv_listesi')




#------------------------------------------------------------------------------------

@login_required
def opr_admin(request, pk=None):

    if not request.user.is_superuser:
        mesaj = "kullanıcı sistem yöneticisi değil...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})


    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = SirketSecForm(request.POST)
        print("şirketform okundu...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            gelen_sirket = request.POST.get('sirket', "")
            print("sirket....", sirket)
            secili_sirket = sirket.objects.get(id=gelen_sirket)
            kisi_listesi = Profile.objects.filter(sirket=gelen_sirket)
            if not kisi_listesi:
                mesaj = "bu şirkete ait kullanıcı yok...!!"
                return render(request, 'islem/uyari.html', {'mesaj': mesaj})

            opr_admin_list = kisi_listesi.filter(opr_admin="E")
            kisi_list = kisi_listesi.filter(opr_admin="H")
            contx_dict = {'kisi_list': kisi_list, 'opr_admin_list': opr_admin_list, 'sirket': secili_sirket}
            return render(request, 'islem/sirket_kisi_list.html', contx_dict)
        else:
            print(" geçerli değil............")
            return render(request, 'islem/sirket_form.html', {'form': form,})
    # if a GET (or any other method) we'll create a blank form
    else:
        #form = SpvForm(serbest_spv=kalan_list)
        form = SirketSecForm()
        return render(request, 'islem/sirket2_form.html', {'form': form,})




@login_required
def opr_admin_ekle(request, pk=None):
    # if this is a POST request we need to process the form data
    user_obj = get_object_or_404(Profile, pk=pk)
    if user_obj.opr_admin == "E":
        mesaj = "bu kişi zaten şirket sistem yöneticisi...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    print("user profile obj....", user_obj)
    context = {'user_obj' : user_obj,
              }
    return render(request, 'islem/opr_admin_ekle_soru.html', context )



@login_required
def opr_admin_ekle_kesin(request, pk=None):
    #user_obj = Profile.objects.get(id=pk)
    user_obj = get_object_or_404(Profile, pk=pk)
    if user_obj.opr_admin == "E":
        mesaj = "bu kişi zaten şirket sistem yöneticisi...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    user_obj.opr_admin = "E"
    user_obj.save()
    return redirect('opr_admin')






@login_required
def opr_admin_kaldir(request, pk=None):
    # if this is a POST request we need to process the form data
    user_obj = get_object_or_404(Profile, pk=pk)
    if user_obj.opr_admin == "E":
        mesaj = "bu kişi zaten şirket sistem yöneticisi...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    print("user profile obj....", user_obj)
    context = {'user_obj' : user_obj,
              }
    return render(request, 'islem/opr_admin_kaldir_soru.html', context )




@login_required
def opr_admin_kaldir_kesin(request, pk=None):
    user_obj = get_object_or_404(Profile, pk=pk)
    if user_obj.opr_admin == "H":
        mesaj = "bu kişi zaten şirket sistem yöneticisi  değil...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    print("user profile obj....", user_obj)
    user_obj.opr_admin = "H"
    user_obj.save()
    return redirect('opr_admin')






#------------------------------------------------------------------------------------




@login_required
def den_listesi(request, pk=None):
    secili_sirket = request.user.profile.sirket
    print("işte kişinin şirketi...", secili_sirket)
    if not secili_sirket:
        mesaj = "kişinin bağlı olduğu şirket yok...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    den_obj = den_yetkilisi.objects.filter(sirket=secili_sirket)
    grup_list = []
    grupdisi_list = []

    for den in den_obj:
        kisi = den.den_yetkilisi.id
        kisi_obj = User.objects.get(id=kisi)
        print("kişi object...", kisi_obj)
        kisi_sirket = kisi_obj.profile.sirket
        print("kişi şirket..", kisi_sirket)
        if kisi_sirket:
            if kisi_sirket.turu == "P":
                grup_list.append(kisi_obj)
            else:
                grupdisi_list.append(kisi_obj)

    print("grup list..", grup_list)
    print("grup dışı list..", grupdisi_list)
    context = {'grup_list': grup_list, 'grupdisi_list': grupdisi_list}
    return render(request, 'islem/den_list.html', context )



@login_required
def den_yarat(request, pk=None):
    # if this is a POST request we need to process the form data
    kullanici = request.user
    sirket = kullanici.profile.sirket
    denler_obj = Profile.objects.filter(denetci="E")

    serbest_den_list = []
    for den in denler_obj:
        if den.sirket.turu == "D":
            usr_obj = den.user
            serbest_den_list.append(usr_obj)
    print("serbest denetci...", serbest_den_list)

    den_obj = den_yetkilisi.objects.filter(sirket=sirket)
    grupdisi_list = []
    for den in den_obj:
        kisi = den.den_yetkilisi.id
        kisi_obj = User.objects.get(id=kisi)
        print("kişi object...", kisi_obj)
        kisi_sirket = kisi_obj.profile.sirket
        print("kişi şirket..", kisi_sirket)
        if kisi_sirket:
            if kisi_sirket.turu == "D":
                grupdisi_list.append(kisi_obj)
    print("grup dışı list  dışarıdan şirkete atanmış olanlar.......", grupdisi_list)

    kalan_list = list(set(serbest_den_list) - set(grupdisi_list))

    print("kontrolden sonra serbest denetci...", kalan_list)

    if not kalan_list:
        mesaj = "eklenecek süpervizör yok...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        #form = SpvForm(request.POST, serbest_spv=kalan_list)
        form = DenForm(request.POST)
        print("denform okundu...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            den_yetkili = request.POST.getlist('den', "")
            print("den yetkili....", den_yetkili)
            for x in den_yetkili:
                kaydetme_obj = den_yetkilisi(den_yetkilisi_id=x, sirket_id=sirket.id)
                kaydetme_obj.save()
            return redirect('den_listesi')
        else:
            print(" geçerli değil............")
            return render(request, 'islem/den_form.html', {'form': form,})
    # if a GET (or any other method) we'll create a blank form
    else:

        #form = SpvForm(serbest_spv=kalan_list)
        form = SpvForm()
        return render(request, 'islem/den_form.html', {'form': form,})




@login_required
def den_listesi_sil(request, pk=None):
    # if this is a POST request we need to process the form data
    user_obj = User.objects.get(id=pk)
    kullanici = request.user
    sirket = kullanici.profile.sirket
    den_obj = den_yetkilisi.objects.filter(den_yetkilisi=user_obj.id).filter(sirket=sirket)
    print("den object....", den_obj)
    print("den listesi sil içinden den obj..", den_obj)
    context = {'den_obj' : den_obj,
              }
    return render(request, 'islem/den_sil_soru.html', context )



@login_required
def den_listesi_sil_kesin(request, pk=None):
    user_obj = User.objects.get(id=pk)
    kullanici = request.user
    sirket = kullanici.profile.sirket
    den_obj = den_yetkilisi.objects.filter(den_yetkilisi=user_obj.id).filter(sirket=sirket)
    #object = get_object_or_404(spv_yetkilisi, pk=pk)
    try:
        den_obj.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    messages.success(request, 'Başarıyla silindi')
    return redirect('den_listesi')








#------------------------------------------------------------------------------------







import copy



@login_required
def yer_detay(request, pk=None):
    yer_obj = yer.objects.get(id=pk)
    print("yer objesi...", yer_obj)
    opr_obj = plan_opr_gun.objects.filter(yer=pk)
    den_obj = plan_den_gun.objects.filter(yer=pk)
    print("opr obj....", opr_obj)
    print("den obj....", den_obj)
    o_pzt_arr = []
    o_sal_arr = []
    o_car_arr = []
    o_per_arr = []
    o_cum_arr = []
    o_cmt_arr = []
    o_paz_arr = []
    d_pzt_arr = []
    d_sal_arr = []
    d_car_arr = []
    d_per_arr = []
    d_cum_arr = []
    d_cmt_arr = []
    d_paz_arr = []


    pzt_obj = opr_obj.filter(gun="Pzt")
    print("pzt obj........................................", pzt_obj)
    sal_obj = opr_obj.filter(gun="Sal")
    print("sal obj........................................", sal_obj)
    car_obj = opr_obj.filter(gun="Çar")
    print("car obj........................................", car_obj)
    per_obj = opr_obj.filter(gun="Per")
    print("per obj........................................", per_obj)
    cum_obj = opr_obj.filter(gun="Cum")
    print("cum obj........................................", cum_obj)
    cmt_obj = opr_obj.filter(gun="Cmt")
    print("cmt obj........................................", cmt_obj)
    paz_obj = opr_obj.filter(gun="Paz")
    print("paz obj........................................", paz_obj)

    pzt_oc = pzt_obj.count()
    sal_oc = sal_obj.count()
    car_oc = car_obj.count()
    per_oc = per_obj.count()
    cum_oc = cum_obj.count()
    cmt_oc = cmt_obj.count()
    paz_oc = paz_obj.count()

    max_oc = pzt_oc
    if sal_oc > max_oc:
        max_oc = sal_oc
    if car_oc > max_oc:
        max_oc = car_oc
    if per_oc > max_oc:
        max_oc = per_oc
    if cum_oc > max_oc:
        max_oc = cum_oc
    if cmt_oc > max_oc:
        max_oc = cmt_oc
    if paz_oc > max_oc:
        max_oc = paz_oc

    print("en yüksek işlem sayısı...", max_oc)

    for pzt in pzt_obj:
        temp=[pzt.zaman, pzt]
        o_pzt_arr.append(temp)
    o_pzt_arr.sort()
    fark = max_oc - pzt_oc
    if fark != 0:
        while fark !=0:
            o_pzt_arr.append(None)
            fark = fark - 1

    for sal in sal_obj:
        temp=[sal.zaman, sal]
        o_sal_arr.append(temp)
    o_sal_arr.sort()
    fark = max_oc - sal_oc
    if fark != 0:
        while fark !=0:
            o_sal_arr.append(None)
            fark = fark - 1

    for car in car_obj:
        temp=[car.zaman, car]
        o_car_arr.append(temp)
    o_car_arr.sort()
    fark = max_oc - car_oc
    if fark != 0:
        while fark !=0:
            o_car_arr.append(None)
            fark = fark - 1

    for per in per_obj:
        temp=[per.zaman, per]
        o_per_arr.append(temp)
    o_per_arr.sort()
    fark = max_oc - per_oc
    if fark != 0:
        while fark !=0:
            o_per_arr.append(None)
            fark = fark - 1

    for cum in cum_obj:
        temp=[cum.zaman, cum]
        o_cum_arr.append(temp)
    o_cum_arr.sort()
    fark = max_oc - cum_oc
    if fark != 0:
        while fark !=0:
            o_cum_arr.append(None)
            fark = fark - 1

    for cmt in cmt_obj:
        temp=[cmt.zaman, cmt]
        o_cmt_arr.append(temp)
    o_cmt_arr.sort()
    fark = max_oc - cmt_oc
    if fark != 0:
        while fark !=0:
            o_cmt_arr.append(None)
            fark = fark - 1

    for paz in paz_obj:
        temp=[paz.zaman, paz]
        o_paz_arr.append(temp)
    o_paz_arr.sort()
    fark = max_oc - paz_oc
    if fark != 0:
        while fark !=0:
            o_paz_arr.append(None)
            fark = fark - 1

    print("pzt list...bakalım...", o_pzt_arr)
    print("sal list...bakalım...", o_sal_arr)
    print("car list...bakalım...", o_car_arr)
    print("per list...bakalım...", o_per_arr)
    print("cum list...bakalım...", o_cum_arr)
    print("cmt list...bakalım...", o_cmt_arr)
    print("paz list...bakalım...", o_paz_arr)


    o_list = []
    i = 0
    while i < max_oc:
        g_list = []
        g_list.append(o_pzt_arr[i])
        g_list.append(o_sal_arr[i])
        g_list.append(o_car_arr[i])
        g_list.append(o_per_arr[i])
        g_list.append(o_cum_arr[i])
        g_list.append(o_cmt_arr[i])
        g_list.append(o_paz_arr[i])
        o_list.append(g_list)
        i = i + 1

    print("işte o list...sonunda..", o_list)



    pzt_obj = den_obj.filter(gun="Pzt")
    print("pzt obj........................................", pzt_obj)
    sal_obj = den_obj.filter(gun="Sal")
    print("sal obj........................................", sal_obj)
    car_obj = den_obj.filter(gun="Çar")
    print("car obj........................................", car_obj)
    per_obj = den_obj.filter(gun="Per")
    print("per obj........................................", per_obj)
    cum_obj = den_obj.filter(gun="Cum")
    print("cum obj........................................", cum_obj)
    cmt_obj = den_obj.filter(gun="Cmt")
    print("cmt obj........................................", cmt_obj)
    paz_obj = den_obj.filter(gun="Paz")
    print("paz obj........................................", paz_obj)

    pzt_dc = pzt_obj.count()
    sal_dc = sal_obj.count()
    car_dc = car_obj.count()
    per_dc = per_obj.count()
    cum_dc = cum_obj.count()
    cmt_dc = cmt_obj.count()
    paz_dc = paz_obj.count()

    max_dc = pzt_dc
    if sal_dc > max_dc:
        max_dc = sal_dc
    if car_dc > max_dc:
        max_dc = car_dc
    if per_dc > max_dc:
        max_dc = per_dc
    if cum_dc > max_dc:
        max_dc = cum_dc
    if cmt_dc > max_dc:
        max_dc = cmt_dc
    if paz_dc > max_dc:
        max_dc = paz_dc

    print("en yüksek denetim sayısı...", max_dc)

    for pzt in pzt_obj:
        temp=[pzt.zaman, pzt]
        d_pzt_arr.append(temp)
    d_pzt_arr.sort()
    fark = max_dc - pzt_dc
    if fark != 0:
        while fark !=0:
            d_pzt_arr.append(None)
            fark = fark - 1

    for sal in sal_obj:
        temp=[sal.zaman, sal]
        d_sal_arr.append(temp)
    d_sal_arr.sort()
    fark = max_dc - sal_dc
    if fark != 0:
        while fark !=0:
            d_sal_arr.append(None)
            fark = fark - 1

    for car in car_obj:
        temp=[car.zaman, car]
        d_car_arr.append(temp)
    d_car_arr.sort()
    fark = max_dc - car_dc
    if fark != 0:
        while fark !=0:
            d_car_arr.append(None)
            fark = fark - 1

    for per in per_obj:
        temp=[per.zaman, per]
        d_per_arr.append(temp)
    d_per_arr.sort()
    fark = max_dc - per_dc
    if fark != 0:
        while fark !=0:
            d_per_arr.append(None)
            fark = fark - 1

    for cum in cum_obj:
        temp=[cum.zaman, cum]
        d_cum_arr.append(temp)
    d_cum_arr.sort()
    fark = max_dc - cum_dc
    if fark != 0:
        while fark !=0:
            d_cum_arr.append(None)
            fark = fark - 1

    for cmt in cmt_obj:
        temp=[cmt.zaman, cmt]
        d_cmt_arr.append(temp)
    d_cmt_arr.sort()
    fark = max_dc - cmt_dc
    if fark != 0:
        while fark !=0:
            d_cmt_arr.append(None)
            fark = fark - 1

    for paz in paz_obj:
        temp=[paz.zaman, paz]
        d_paz_arr.append(temp)
    d_paz_arr.sort()
    fark = max_dc - paz_dc
    if fark != 0:
        while fark !=0:
            d_paz_arr.append(None)
            fark = fark - 1

    print("pzt list...bakalım...", d_pzt_arr)
    print("sal list...bakalım...", d_sal_arr)
    print("car list...bakalım...", d_car_arr)
    print("per list...bakalım...", d_per_arr)
    print("cum list...bakalım...", d_cum_arr)
    print("cmt list...bakalım...", d_cmt_arr)
    print("paz list...bakalım...", d_paz_arr)


    d_list = []
    i = 0
    while i < max_dc:
        g_list = []
        g_list.append(d_pzt_arr[i])
        g_list.append(d_sal_arr[i])
        g_list.append(d_car_arr[i])
        g_list.append(d_per_arr[i])
        g_list.append(d_cum_arr[i])
        g_list.append(d_cmt_arr[i])
        g_list.append(d_paz_arr[i])
        d_list.append(g_list)
        i = i + 1

    print("işte d list...sonunda..", d_list)


    context = {'yer': yer_obj,
               'o_list': o_list,
               'd_list': d_list,
               'max_oc': max_oc,
               'max_dc': max_dc,
               }
    return render(request, 'islem/yer_detay.html', context)








import time



@login_required
@transaction.atomic
def yer_operasyon_planla(request, pk=None):
    # eski takılan yada yeniden planlanacak yerler için....
    print("operasyon planlama için gelen id...", pk)
    yer_obj = yer.objects.get(id=pk)
    print("valid-- operasyon dilimleri", yer_obj.opr_basl, "-", yer_obj.opr_son, "-", yer_obj.opr_delta)
    # burada günlük operasyon ve denetim dosyası oluşturulacak.....
    gun_arr = ['Pzt','Sal','Çar','Per','Cum','Cmt','Paz',]
    i = 0
    while i < 7:
        h1, m1, s1 = yer_obj.opr_basl.hour, yer_obj.opr_basl.minute, yer_obj.opr_basl.second
        print("okunan time değerleri...", h1, "-", m1, "-", s1)
        total_sec = 3600*h1+60*m1+s1
        saat = datetime.timedelta(0,total_sec,0)
        h1, m1, s1 = yer_obj.opr_delta.hour, yer_obj.opr_delta.minute, yer_obj.opr_delta.second
        print("okunan time değerleri...", h1, "-", m1, "-", s1)
        total_sec = 3600*h1+60*m1+s1
        fark_opr = datetime.timedelta(0,total_sec,0)
        h1, m1, s1 = yer_obj.opr_son.hour, yer_obj.opr_son.minute, yer_obj.opr_son.second
        print("okunan time değerleri...", h1, "-", m1, "-", s1)
        total_sec = 3600*h1+60*m1+s1
        son_saat = datetime.timedelta(0,total_sec,0)
        print("işte saat, fark ve son saat.. timedelta olarak...", saat, "-", fark_opr, "-", son_saat)
        while saat <= son_saat:
            saniyeler = saat.seconds
            h1 = saniyeler // 3600
            k1 = saniyeler % 3600
            m1 = k1 // 60
            s1 = k1 % 60
            print("hesaplanan time değerleri saniyeden dönüştürme..", h1, "-", m1, "-", s1)
            kay_saat = datetime.time(h1,m1,s1)
            print("kaydetme saati...", kay_saat)
            kaydetme_obj = plan_opr_gun(yer_id=yer_obj.id, gun=gun_arr[i], zaman=kay_saat)
            kaydetme_obj.save()
            print("kaydetme objedeki saat...", saat)
            saat = saat + fark_opr
        i = i + 1
    return redirect('yer_detay', pk=pk)



@login_required
def yer_operasyon_ekle(request, pk=None):
    yer_obj = yer.objects.get(id=pk)
    print("yer objesi...", yer_obj)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GunForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            post = form.save(commit=False)
            post.yer = yer_obj
            post.save()
            messages.success(request, 'Operasyon saati kaydedildi')
            return redirect('yer_detay', pk=pk)
        else:
            messages.success(request, 'Formda uygunsuzluk var')
            return render(request, 'islem/yer_operasyon_yarat.html', {'form': form, 'yer_obj':yer_obj})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GunForm()
        return render(request, 'islem/yer_operasyon_yarat.html', {'form': form, 'yer_obj':yer_obj})



@login_required
def yer_operasyon_duzenle(request, pk=None, pk2=None):
    yer_obj = yer.objects.get(id=pk)
    print("yer objesi...", yer_obj)
    plan_opr_obj = plan_opr_gun.objects.get(id=pk2)
    print("plan opr obj...", plan_opr_obj)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SaatForm(request.POST, instance=plan_opr_obj)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            messages.success(request, 'Operasyon saati kaydedildi')
            return redirect('yer_detay', pk=pk)
        else:
            messages.success(request, 'Formda uygunsuzluk var')
            return redirect('yer_operasyon_duzenle', pk=pk, pk2=pk2)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SaatForm(instance=plan_opr_obj)
        return render(request, 'islem/yer_operasyon_duzenle.html', {'form': form, 'plan_opr_obj':plan_opr_obj, })




@login_required
def yer_operasyon_sil(request, pk=None, pk2=None):
    yer_obj = yer.objects.get(id=pk)
    print("yer objesi...", yer_obj)
    opr_plan_obj = plan_opr_gun.objects.get(id=pk2)
    return render(request, 'islem/yer_opr_sil_soru.html', {'opr_plan_obj': opr_plan_obj,})



@login_required
def yer_operasyon_sil_kesin(request, pk=None, pk2=None):
    print("tipi sil kesindeki pk:", pk)
    #object = get_object_or_404(plan_opr_gun, pk=pk2)
    object = plan_opr_gun.objects.get(id=pk2)
    try:
        object.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    messages.success(request, 'Başarıyla silindi')
    return redirect('yer_detay', pk=pk)



#----------------------------------------------------------------------------------------------
#   yer denetim işlemleri




@login_required
@transaction.atomic
def yer_denetim_planla(request, pk=None):
    # eski takılan yada yeniden planlanacak yerler için....
    print("operasyon planlama için gelen id...", pk)
    yer_obj = yer.objects.get(id=pk)
    print("valid-- operasyon dilimleri", yer_obj.opr_basl, "-", yer_obj.opr_son, "-", yer_obj.opr_delta)
    # burada günlük operasyon ve denetim dosyası oluşturulacak.....
    gun_arr = ['Pzt','Sal','Çar','Per','Cum','Cmt','Paz',]
    i = 0
    while i < 7:
        h1, m1, s1 = yer_obj.den_basl.hour, yer_obj.den_basl.minute, yer_obj.den_basl.second
        print("okunan time değerleri...", h1, "-", m1, "-", s1)
        total_sec = 3600*h1+60*m1+s1
        saat = datetime.timedelta(0,total_sec,0)
        h1, m1, s1 = yer_obj.den_delta.hour, yer_obj.den_delta.minute, yer_obj.den_delta.second
        print("okunan time değerleri...", h1, "-", m1, "-", s1)
        total_sec = 3600*h1+60*m1+s1
        fark_opr = datetime.timedelta(0,total_sec,0)
        h1, m1, s1 = yer_obj.den_son.hour, yer_obj.den_son.minute, yer_obj.den_son.second
        print("okunan time değerleri...", h1, "-", m1, "-", s1)
        total_sec = 3600*h1+60*m1+s1
        son_saat = datetime.timedelta(0,total_sec,0)
        print("işte saat, fark ve son saat.. timedelta olarak...", saat, "-", fark_opr, "-", son_saat)
        while saat <= son_saat:
            saniyeler = saat.seconds
            h1 = saniyeler // 3600
            k1 = saniyeler % 3600
            m1 = k1 // 60
            s1 = k1 % 60
            print("hesaplanan time değerleri saniyeden dönüştürme..", h1, "-", m1, "-", s1)
            kay_saat = datetime.time(h1,m1,s1)
            print("kaydetme saati...", kay_saat)
            kaydetme_obj = plan_den_gun(yer_id=yer_obj.id, gun=gun_arr[i], zaman=kay_saat)
            kaydetme_obj.save()
            print("kaydetme objedeki saat...", saat)
            saat = saat + fark_opr
        i = i + 1
    return redirect('yer_detay', pk=pk)



@login_required
def yer_denetim_ekle(request, pk=None):
    yer_obj = yer.objects.get(id=pk)
    print("yer objesi...", yer_obj)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GunDenForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            post = form.save(commit=False)
            post.yer = yer_obj
            post.save()
            messages.success(request, 'Operasyon saati kaydedildi')
            return redirect('yer_detay', pk=pk)
        else:
            messages.success(request, 'Formda uygunsuzluk var')
            return render(request, 'islem/yer_denetim_yarat.html', {'form': form, 'yer_obj':yer_obj})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GunDenForm()
        return render(request, 'islem/yer_denetim_yarat.html', {'form': form, 'yer_obj':yer_obj})



@login_required
def yer_denetim_duzenle(request, pk=None, pk2=None):
    yer_obj = yer.objects.get(id=pk)
    print("yer objesi...", yer_obj)
    plan_den_obj = plan_den_gun.objects.get(id=pk2)
    print("plan opr obj...", plan_den_obj)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SaatDenForm(request.POST, instance=plan_den_obj)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            messages.success(request, 'Operasyon saati kaydedildi')
            return redirect('yer_detay', pk=pk)
        else:
            messages.success(request, 'Formda uygunsuzluk var')
            return render(request, 'islem/yer_denetim_duzenle.html', {'form': form, 'plan_den_obj':plan_den_obj, })

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SaatDenForm(instance=plan_den_obj)
        return render(request, 'islem/yer_denetim_duzenle.html', {'form': form, 'plan_den_obj':plan_den_obj, })




@login_required
def yer_denetim_sil(request, pk=None, pk2=None):
    yer_obj = yer.objects.get(id=pk)
    print("yer objesi...", yer_obj)
    den_plan_obj = plan_den_gun.objects.get(id=pk2)
    return render(request, 'islem/yer_den_sil_soru.html', {'den_plan_obj': den_plan_obj,})



@login_required
def yer_denetim_sil_kesin(request, pk=None, pk2=None):
    print("tipi sil kesindeki pk:", pk)
    #object = get_object_or_404(plan_opr_gun, pk=pk2)
    object = plan_den_gun.objects.get(id=pk2)
    try:
        object.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    messages.success(request, 'Başarıyla silindi')
    return redirect('yer_detay', pk=pk)



#---------------------------------------------------------------------------------


@login_required
def qrdosyasi_create(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Qrcode_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            denetim = request.POST.get('denetim', "")
            qrcode = request.POST.get('qrcode', "")
            print ("denetim....", denetim)
            print("qrcode...", qrcode)
            request.session['denetim_qrcode'] = denetim
            request.session['qrdosyasi_qrcode'] = qrcode

            qr_obj = qrdosyasi.objects.filter(qr_deger=qrcode).first()

            if qr_obj:
                messages.success(request, 'QRCode zaten tanımlı')
                return redirect('qrdosyasi_create')
            else:
                kaydetme_obj = qrdosyasi(qr_deger=qrcode, denetim_id=denetim)
                kaydetme_obj.save()
                messages.success(request, 'Başarıyla kaydetti')
                return redirect('qrdosyasi_create')
        else:
            messages.success(request, 'Formda uygunsuzluk var')
            return redirect('qrdosyasi_create')
            #return render(request, 'islem/denetim_deneme_form.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        #selected_alt = request.session.get('selected_alt')
        form = Qrcode_Form()
        return render(request, 'islem/qrdosyasi_form.html', {'form': form,})





#---------------------------------------------------------------------------------


@login_required
def qrdosyasi_update(request, pk=None):
    # if this is a POST request we need to process the form data
    qrdosyasi_no = pk

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Qrcode_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("valid")
            denetim = request.POST.get('denetim', "")
            qrcode = request.POST.get('qrcode', "")
            print ("denetim", denetim)
            print("qrcode...", qrcode)
            request.session['denetim_qrcode'] = denetim
            request.session['qrdosyasi_qrcode'] = qrcode
            kaydetme_obj = qrdosyasi(id=pk, qr_deger=qrcode, denetim_id=denetim)
            kaydetme_obj.save()
            messages.success(request, 'Başarıyla düzenledi')
            return redirect('qrdosyasi_update')
        else:
            messages.success(request, 'Formda uygunsuzluk var')
            return redirect('qrdosyasi_update')
            #return render(request, 'islem/denetim_deneme_form.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        #selected_alt = request.session.get('selected_alt')
        qr_obj = qrdosyasi.objects.get(id=qrdosyasi_no)
        form = Qrcode_Form()
        form.fields["denetim"].initial = qr_obj.denetim
        form.fields["qrcode"].initial = qr_obj.qr_deger
        return render(request, 'islem/qrdosyasi_form2.html', {'form': form,})





#------------------------------------------------------------------
#  denetimi tamamlama işlemleri önce sor sonra tamamla

@login_required
def qrdosyasi_sil(request, pk=None):

    qrdosyasi_obj = qrdosyasi.objects.get(id=pk)
    print("seçilen qrdosyasi", qrdosyasi_obj)
    numarasi = qrdosyasi_obj.id
    denetim_adi = qrdosyasi_obj.denetim
    qrcode = qrdosyasi_obj.qr_deger
    context = {'denetim_adi': denetim_adi,
               'numarasi' : numarasi,
               'qrcode' : qrcode,
              }
    return render(request, 'islem/qrdosyasi_iptal_sor.html', context )


#--------------------------------------------------------------------------------

# denetim iptal ediliyor Y yapılıyor....

@login_required
def qrdosyasi_sil_kesin(request, pk=None):

    qrdosyasi_obj = qrdosyasi.objects.get(id=pk)
    print("seçilen qrdosyasi", qrdosyasi_obj)

    qrdosyasi_obj.delete()
    messages.success(request, 'QRCode iptal edildi')
    return redirect('qrdosyasi')
    #return render(request, 'islem/tipi_sil_soru.html', args)

#---------------------------------------------------------------------------------



@login_required
def tipi_sil(request, pk=None):
    print("tipi sildeki pk:", pk)
    object = get_object_or_404(tipi, pk=pk)
    sil_tipi = object.tipi_adi
    sil_id = object.id
    print("sil_tipi", sil_tipi)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_tipi': sil_tipi, 'pk': pk,}
    return render(request, 'islem/tipi_sil_soru.html', args)


@login_required
def tipi_sil_kesin(request, pk=None):
    print("tipi sil kesindeki pk:", pk)
    object = get_object_or_404(tipi, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    messages.success(request, 'Başarıyla silindi')
    return redirect('tipi')


#------------------------------------------------------



@login_required
def zon_sil(request, pk=None):
    print("zon sildeki pk:", pk)
    object = get_object_or_404(zon, pk=pk)
    sil_zon = object.zon_adi
    sil_id = object.id
    print("sil_zon", sil_zon)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_zon': sil_zon, 'pk': pk,}
    return render(request, 'islem/zon_sil_soru.html', args)


@login_required
def zon_sil_kesin(request, pk=None):
    print("zon sil kesindeki pk:", pk)
    object = get_object_or_404(zon, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    messages.success(request, 'Başarıyla silindi')
    return redirect('zon')


#------------------------------------------------------



@login_required
def bolum_sil(request, pk=None):
    print("bolum sildeki pk:", pk)
    object = get_object_or_404(bolum, pk=pk)
    sil_bolum = object.bolum_adi
    sil_id = object.id
    print("sil_bolum", sil_bolum)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_bolum': sil_bolum, 'pk': pk,}
    return render(request, 'islem/bolum_sil_soru.html', args)


@login_required
def bolum_sil_kesin(request, pk=None):
    print("bolum sil kesindeki pk:", pk)
    object = get_object_or_404(bolum, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    messages.success(request, 'Başarıyla silindi')
    return redirect('bolum')

#------------------------------------------------------

@login_required
def detay_sil(request, pk=None):
    print("detay sildeki pk:", pk)
    object = get_object_or_404(detay, pk=pk)
    sil_detay = object.detay_adi
    sil_id = object.id
    print("sil_detay", sil_detay)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_detay': sil_detay, 'pk': pk,}
    return render(request, 'islem/detay_sil_soru.html', args)


@login_required
def detay_sil_kesin(request, pk=None):
    print("detay sil kesindeki pk:", pk)
    object = get_object_or_404(detay, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    messages.success(request, 'Başarıyla silindi')
    return redirect('detay')


#------------------------------------------------------

@login_required
def projealanlari_listele(request):
    user = request.user
    if proje_varmi_kontrol(request):
        print("proje var mı kontrolden geçtik.....")
        proje = user.profile.proje
        pa_obj = proje_alanlari.objects.filter(proje=proje)
        return render(request, 'islem/proje_alanlari_list.html', {'proje_alanlari_list': pa_obj,})

    else:
        print("buraya geldi...proje yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})



@login_required
def projealanlari_yarat(request):
    # if this is a POST request we need to process the form data
    kullanici = request.user
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PAForm(request.POST, kullanici=kullanici)
        # check whether it's valid:
        if form.is_valid():
            print("valid")
            post = form.save(commit=False)
            post.save()
            messages.success(request, 'Başarıyla kaydetti')
            return redirect('projealanlari_listele')
        else:
            return render(request, 'islem/proje_alanlari_form.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        print(" paform get alanı için...")
        form = PAForm(kullanici=kullanici)
        print("pa form tanımdan sonra...")
        return render(request, 'islem/proje_alanlari_form.html', {'form': form,})



@login_required
def projealanlari_sil(request, pk=None):
    print("proje alanlari sildeki pk:", pk)
    pa_object = get_object_or_404(proje_alanlari, pk=pk)
    args = {'pa_object': pa_object,}
    return render(request, 'islem/proje_alanlari_sil_soru.html', args)


@login_required
def projealanlari_sil_kesin(request, pk=None):
    print("detay sil kesindeki pk:", pk)
    object = get_object_or_404(proje_alanlari, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})

    messages.success(request, 'Başarıyla silindi')
    return redirect('projealanlari_listele')

#------------------------------------------------------


@login_required
def yer_listele(request):
    user = request.user
    if proje_varmi_kontrol(request):
        print("proje var mı kontrolden geçtik.")
        proje = user.profile.proje
        qs = yer.objects.none()
        projealanlari_obj = proje_alanlari.objects.filter(proje=proje)
        for x in projealanlari_obj:
            qx = yer.objects.filter(proje_alanlari=x.id)
            qs = qs.union(qx)
        qs = qs.order_by('id')
        return render(request, 'islem/yer_list.html', {'yer_list': qs,})

    else:
        print("buraya geldi...proje yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})



@transaction.atomic
@login_required
def yer_yarat(request):
    # if this is a POST request we need to process the form data
    kullanici = request.user
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = YerForm(request.POST, kullanici=kullanici)
        # check whether it's valid:
        if form.is_valid():
            post = form.save(commit=False)
            mac_no_gelen = post.mac_no
            yer_varmi_obj = yer.objects.filter(mac_no=mac_no_gelen).first()

            if yer_varmi_obj:
                print("yer var mı yeni obj ++++++++++++++++++++++", yer_varmi_obj.mac_no)
                p_alani = yer_varmi_obj.proje_alanlari
                proje_a = proje.objects.filter(proje_alanlari=p_alani).first()
                mesaj = "bu mac-no şu anda tanımlı, proje:"+str(proje_a)+" /proje alanı:"+str(p_alani)+" /mac-no:"+str(mac_no_gelen)
                return render(request, 'islem/yer_form.html', {'form': form, 'mesaj': mesaj})

            post.save()
            print("valid-- operasyon dilimleri", post.opr_basl, "-", post.opr_son, "-", post.opr_delta)
            print("valid-- denetim dilimleri", post.den_basl, "-", post.den_son, "-", post.den_delta)
            # burada günlük operasyon ve denetim dosyası oluşturulacak.....
            gun_arr = ['Pzt','Sal','Çar','Per','Cum','Cmt','Paz',]
            i = 0
            while i < 7:
                h1, m1, s1 = post.opr_basl.hour, post.opr_basl.minute, post.opr_basl.second
                print("okunan time değerleri...", h1, "-", m1, "-", s1)
                total_sec = 3600*h1+60*m1+s1
                saat = datetime.timedelta(0,total_sec,0)
                h1, m1, s1 = post.opr_delta.hour, post.opr_delta.minute, post.opr_delta.second
                print("okunan time değerleri...", h1, "-", m1, "-", s1)
                total_sec = 3600*h1+60*m1+s1
                fark_opr = datetime.timedelta(0,total_sec,0)
                h1, m1, s1 = post.opr_son.hour, post.opr_son.minute, post.opr_son.second
                print("okunan time değerleri...", h1, "-", m1, "-", s1)
                total_sec = 3600*h1+60*m1+s1
                son_saat = datetime.timedelta(0,total_sec,0)
                print("işte saat, fark ve son saat.. timedelta olarak...", saat, "-", fark_opr, "-", son_saat)
                while saat <= son_saat:
                    yer_obj = yer.objects.latest('id')
                    saniyeler = saat.seconds
                    h1 = saniyeler // 3600
                    k1 = saniyeler % 3600
                    m1 = k1 // 60
                    s1 = k1 % 60
                    print("hesaplanan time değerleri saniyeden dönüştürme..", h1, "-", m1, "-", s1)
                    kay_saat = datetime.time(h1,m1,s1)
                    print("kaydetme saati...", kay_saat)
                    kaydetme_obj = plan_opr_gun(yer_id=yer_obj.id, gun=gun_arr[i], zaman=kay_saat)
                    kaydetme_obj.save()
                    print("kaydetme objedeki saat...", saat)
                    saat = saat + fark_opr
                i = i + 1

            i = 0
            while i < 7:
                h1, m1, s1 = post.den_basl.hour, post.den_basl.minute, post.den_basl.second
                print("okunan time değerleri...", h1, "-", m1, "-", s1)
                total_sec = 3600*h1+60*m1+s1
                saat = datetime.timedelta(0,total_sec,0)
                h1, m1, s1 = post.den_delta.hour, post.den_delta.minute, post.den_delta.second
                print("okunan time değerleri...", h1, "-", m1, "-", s1)
                total_sec = 3600*h1+60*m1+s1
                fark_opr = datetime.timedelta(0,total_sec,0)
                h1, m1, s1 = post.den_son.hour, post.den_son.minute, post.den_son.second
                print("okunan time değerleri...", h1, "-", m1, "-", s1)
                total_sec = 3600*h1+60*m1+s1
                son_saat = datetime.timedelta(0,total_sec,0)
                print("işte saat, fark ve son saat.. timedelta olarak...", saat, "-", fark_opr, "-", son_saat)
                while saat <= son_saat:
                    yer_obj = yer.objects.latest('id')
                    saniyeler = saat.seconds
                    h1 = saniyeler // 3600
                    k1 = saniyeler % 3600
                    m1 = k1 // 60
                    s1 = k1 % 60
                    print("hesaplanan time değerleri saniyeden dönüştürme..", h1, "-", m1, "-", s1)
                    kay_saat = datetime.time(h1,m1,s1)
                    print("kaydetme saati...", kay_saat)
                    kaydetme_obj = plan_den_gun(yer_id=yer_obj.id, gun=gun_arr[i], zaman=kay_saat)
                    kaydetme_obj.save()
                    print("kaydetme objedeki saat...", saat)
                    saat = saat + fark_opr
                i = i + 1

            messages.success(request, 'Başarıyla kaydetti')
            return redirect('yer_listele')
        else:
            print ("hatalar...ha ha ha ")
            mesaj = ""
            return render(request, 'islem/yer_form.html', {'form': form, 'mesaj': mesaj})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = YerForm(kullanici=kullanici)
        mesaj = ""
        return render(request, 'islem/yer_form.html', {'form': form, 'mesaj':mesaj})



@login_required
def yer_duzenle(request, pk=None):
    # if this is a POST request we need to process the form data
    kullanici = request.user
    yer_obj = get_object_or_404(yer, pk=pk)
    ilk_mac = yer_obj.mac_no
    print("yer obje ilk okumada....ilk mac ---------------",ilk_mac)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = YerForm(request.POST, kullanici=kullanici, instance=yer_obj)
        # check whether it's valid:
        if form.is_valid():
            print("valid")
            post = form.save(commit=False)
            mac_no_gelen = post.mac_no
            print("mac no gelen --------++++++++++++++++++", mac_no_gelen)
            yer_varmi_obj = yer.objects.filter(mac_no=mac_no_gelen).first()
            print("++++++++++++++++++++++++++....yer_var mı:", yer_varmi_obj)
            print("yer obje - mac no..........", yer_obj.mac_no)
            if ilk_mac == mac_no_gelen:
                print("passsssssss mı geçti  //////////////////")
                pass
            elif yer_varmi_obj:
                print("yer var mı ya geldi....")
                p_alani = yer_varmi_obj.proje_alanlari
                proje_a = proje.objects.filter(proje_alanlari=p_alani).first()
                mesaj = "bu mac-no şu anda tanımlı, proje:"+str(proje_a)+" /proje alanı:"+str(p_alani)+" /mac-no:"+str(mac_no_gelen)
                return render(request, 'islem/yer_form.html', {'form': form, 'mesaj': mesaj})

            post.save()
            messages.success(request, 'Başarıyla kaydetti')
            return redirect('yer_listele')
        else:
            mesaj = ""
            return render(request, 'islem/yer_form.html', {'form': form, 'mesaj': mesaj})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = YerForm(kullanici=kullanici, instance=yer_obj)
        mesaj = ""
        return render(request, 'islem/yer_form.html', {'form': form, 'mesaj': mesaj})



@login_required
def yer_sil(request, pk=None):
    print("detay sildeki pk:", pk)
    sil_object = get_object_or_404(yer, pk=pk)
    args = {'sil_obj': sil_object,}
    return render(request, 'islem/yer_sil_soru.html', args)


@login_required
def yer_sil_kesin(request, pk=None):
    print("yer sil kesindeki pk:", pk)
    object = get_object_or_404(yer, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    messages.success(request, 'Başarıyla silindi')
    return redirect('yer_listele')


#---------------------------------------------------------------------------
# RFID dosya işlemleri....................
# WEB SERVICE OLMADAN................-----


@login_required
def rfid_dosyasi_listele(request):
    user = request.user
    if proje_varmi_kontrol(request):
        print("proje var mı kontrolden geçtik.")
        proje = user.profile.proje
        rfid_dosyasi_obj = rfid_dosyasi.objects.filter(proje=proje).order_by("id")
        return render(request, 'islem/rfid_dosyasi_list.html', {'rfid_dosyasi_list': rfid_dosyasi_obj})

    else:
        print("buraya geldi...proje yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})



@login_required
def rfid_dosyasi_detay(request, pk=None):
    rfid_obj = rfid_dosyasi.objects.get(pk=pk)
    return render(request, 'islem/rfid_dosyasi_detail.html', {'rfid_obj': rfid_obj})




@login_required
def rfid_dosyasi_yarat(request):
    # if this is a POST request we need to process the form data
    kullan = request.user
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RfidForm(request.POST, kullan=kullan)
        # check whether it's valid:
        if form.is_valid():
            print("valid")
            post = form.save(commit=False)
            post.save()
            messages.success(request, 'Başarıyla kaydetti')
            return redirect('rfid_dosyasi_listele')
        else:
            return render(request, 'islem/rfid_dosyasi_form.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RfidForm(kullan=kullan)
        return render(request, 'islem/rfid_dosyasi_form.html', {'form': form,})



@login_required
def rfid_dosyasi_duzenle(request, pk=None):
    # if this is a POST request we need to process the form data
    kullan = request.user
    rfid_dosyasi_obj = get_object_or_404(rfid_dosyasi, pk=pk)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RfidForm(request.POST, kullan=kullan, instance=rfid_dosyasi_obj)
        # check whether it's valid:
        if form.is_valid():
            print("valid")
            post = form.save(commit=False)
            post.save()
            messages.success(request, 'Başarıyla kaydetti')
            return redirect('rfid_dosyasi_listele')
        else:
            return render(request, 'islem/rfid_dosyasi_form.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RfidForm(kullan=kullan, instance=rfid_dosyasi_obj)
        return render(request, 'islem/rfid_dosyasi_form.html', {'form': form,})



@login_required
def rfid_dosyasi_sil(request, pk=None):
    print("grup sildeki pk:", pk)
    rfid_obj = get_object_or_404(rfid_dosyasi, pk=pk)
    args = {'rfid_obj': rfid_obj}
    return render(request, 'islem/rfid_dosyasi_sil_soru.html', args)


@login_required
def rfid_dosyasi_sil_kesin(request, pk=None):
    print("rfid sil kesindeki pk:", pk)
    object = get_object_or_404(rfid_dosyasi, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    messages.success(request, 'Başarıyla silindi')
    return redirect('rfid_dosyasi_listele')





#---------------------------------------------------------------------------
# Çalışan  dosya işlemleri....................


@login_required
def eleman_listele(request):
    user = request.user
    if proje_varmi_kontrol(request):
        print("proje var mı kontrolden geçtik.")
        proje = user.profile.proje
        eleman_obj = eleman.objects.filter(proje=proje).filter(aktifcalisan="E").order_by("id")
        return render(request, 'islem/eleman_list.html', {'eleman_obj': eleman_obj})

    else:
        print("buraya geldi...proje yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})



@login_required
def eleman_detay(request, pk=None):
    eleman_obj = eleman.objects.get(pk=pk)
    return render(request, 'islem/eleman_detail.html', {'eleman_obj': eleman_obj})




@login_required
def eleman_yarat(request):
    # if this is a POST request we need to process the form data
    kullanici = request.user
    proje = kullanici.profile.proje
    sirket = kullanici.profile.sirket

    if not sirket:
        mesaj="kullanıcının şirketi tanımlı değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    if not proje:
        mesaj="kullanıcının projesi tanımlı değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ElemanForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("valid")
            post = form.save(commit=False)
            post.proje = proje
            post.sirket = sirket
            var_mi = eleman.objects.filter(kull_adi=post.kull_adi).filter(sirket=sirket)
            var_count = var_mi.count()
            print("var mı - sonucu...", var_mi, "sayısı", var_count)

            if var_count > 1:
                mesaj = "kişi birden çok kez kayıtlı !"
                return render(request, 'islem/eleman_form.html', {'form': form, 'mesaj': mesaj})
            elif var_count == 1:
                var_olan = var_mi.first()
                print(" var olan kişinin projesi...", var_olan)

                if var_olan.proje == proje:
                    if var_olan.aktifcalisan == "E":
                        mesaj = "kişi bu projede çalışmakta !"
                        return render(request, 'islem/eleman_form.html', {'form': form, 'mesaj': mesaj})
                    else:
                        mesaj = "kişi bu projede çalışmış, tekrar aktif yapın !"
                        return render(request, 'islem/eleman_form.html', {'form': form, 'mesaj': mesaj})
                else:
                    if var_olan.aktifcalisan == "E":
                        mesaj = "kişi "+var_olan.proje +" projesinde çalışmakta  !"
                        return render(request, 'islem/eleman_form.html', {'form': form, 'mesaj': mesaj})
                    else:
                        mesaj = "kişi "+var_olan.proje +" projesinde çalışmış, tekrar aktif yapın  !"
                        return render(request, 'islem/eleman_form.html', {'form': form, 'mesaj': mesaj})
            post.save()
            messages.success(request, 'Başarıyla kaydetti')
            return redirect('eleman_listele')
        else:
            mesaj = ""
            return render(request, 'islem/eleman_form.html', {'form': form, 'mesaj': mesaj})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ElemanForm()
        mesaj = ""
        return render(request, 'islem/eleman_form.html', {'form': form, 'mesaj': mesaj})



@login_required
def eleman_duzenle(request, pk=None):
    # if this is a POST request we need to process the form data
    kullanici = request.user
    eleman_obj = get_object_or_404(eleman, pk=pk)
    proje = kullanici.profile.proje
    sirket = kullanici.profile.sirket
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ElemanForm(request.POST, instance=eleman_obj)
        # check whether it's valid:
        if form.is_valid():
            print("valid")
            post = form.save(commit=False)
            post.proje = proje
            post.sirket = sirket
            if post.kull_adi != eleman_obj.kull_adi:
                mesaj = " vatandaşlık numarası değiştirilemez..!"
                return render(request, 'islem/eleman_form.html', {'form': form, 'mesaj': mesaj})

            post.save()
            messages.success(request, 'Başarıyla kaydetti')
            return redirect('eleman_listele')
        else:
            mesaj=""
            return render(request, 'islem/eleman_form.html', {'form': form, 'mesaj': mesaj})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ElemanForm(instance=eleman_obj)
        mesaj = ""
        return render(request, 'islem/eleman_form.html', {'form': form, 'mesaj': mesaj})



@login_required
def eleman_eskibul(request):
    # if this is a POST request we need to process the form data
    kullanici = request.user
    #eleman_obj = get_object_or_404(eleman, pk=pk)
    proje = kullanici.profile.proje
    sirket = kullanici.profile.sirket
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VatandaslikForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("valid")
            vatno = request.POST.get('vatno', "")
            print("vatno..........", vatno)
            e = eleman.objects.filter(kull_adi=vatno).filter(aktifcalisan="H").first()
            print("el object...", e)
            if e:
                mesaj = ""
                varmi = json.dumps("x")
                ac = json.dumps(e.aktifcalisan)
                context = {'form': form, 'mesaj': mesaj, 'e': e, 'varmi': varmi, 'ac': ac}
                return render(request, 'islem/vatno_form.html', context)
            else:
                mesaj = " aranan kişi eski çalışan değil !"
                varmi = json.dumps("")
                ac = json.dumps("")
                context = {'form': form, 'mesaj': mesaj, 'e': e, 'varmi': varmi, 'ac': ac}
                return render(request, 'islem/vatno_form.html', context)
        else:
            mesaj=""
            e = None
            varmi = json.dumps("")
            ac = json.dumps("")
            context = {'form': form, 'mesaj': mesaj, 'e': e, 'varmi': varmi, 'ac':ac}
            print("context", context)
            return render(request, 'islem/vatno_form.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        print("vatandaşlık get e geldi...")
        form = VatandaslikForm()
        mesaj = ""
        e = None
        varmi = json.dumps("")
        ac = json.dumps("")
        context = {'form': form, 'mesaj': mesaj, 'e': e, 'varmi': varmi, 'ac': ac}
        return render(request, 'islem/vatno_form.html', context)




@login_required
def eleman_eskibul_kesin(request, pk=None):
    print("eleman değiş  kesindeki pk:", pk)
    object = get_object_or_404(eleman, pk=pk)
    #  burada elemanın kaydını al ve update et
    object.aktifcalisan = "E"
    object.save()

    messages.success(request, 'Başarıyla değiştirildi...')
    return redirect('eleman_listele')







#----------------------------------------------
#MK için olan listeleme işlemleri..............
#---------------------------------------------



#------------------------------------------------------

@login_required
def grup_sil(request, pk=None):
    print("grup sildeki pk:", pk)
    object = get_object_or_404(grup, pk=pk)
    sil_grup = object.grup_adi
    sil_id = object.id
    print("sil_grup", sil_grup)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_grup': sil_grup, 'pk': pk,}
    return render(request, 'islem/grup_sil_soru.html', args)


@login_required
def grup_sil_kesin(request, pk=None):
    print("grup sil kesindeki pk:", pk)
    object = get_object_or_404(grup, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    messages.success(request, 'Başarıyla silindi')
    return redirect('grup')


#------------------------------------------------------

@login_required
def sirket_sil(request, pk=None):
    print("sirket sildeki pk:", pk)
    object = get_object_or_404(sirket, pk=pk)
    sil_sirket = object.sirket_adi
    sil_id = object.id
    print("sil_sirket", sil_sirket)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_sirket': sil_sirket, 'pk': pk,}
    return render(request, 'islem/sirket_sil_soru.html', args)


@login_required
def sirket_sil_kesin(request, pk=None):
    print("sirket sil kesindeki pk:", pk)
    object = get_object_or_404(sirket, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    messages.success(request, 'Başarıyla silindi')
    return redirect('sirket')

#------------------------------------------------------

@login_required
def proje_sil(request, pk=None):
    print("proje sildeki pk:", pk)
    object = get_object_or_404(proje, pk=pk)
    sil_proje = object.proje_adi
    sil_id = object.id
    print("sil_proje", sil_proje)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_proje': sil_proje, 'pk': pk,}
    return render(request, 'islem/proje_sil_soru.html', args)


@login_required
def proje_sil_kesin(request, pk=None):
    print("proje sil kesindeki pk:", pk)
    object = get_object_or_404(proje, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        mesaj = "bağlantılı veri var,  silinemez...!!"
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})
    messages.success(request, 'Başarıyla silindi')
    return redirect('proje')


#  .............................................................
#  denetim yaratma işlemleri ...................................
# ..............................................................




class DenetimUpdate(LoginRequiredMixin,UpdateView):
    model = denetim
    fields = ('denetim_adi', 'proje', 'denetci', 'tipi', 'hedef_baslangic', 'hedef_bitis', 'aciklama')
    success_url = "/islem/denetim/"

class DenetimDelete(LoginRequiredMixin,DeleteView):
    model = denetim
    success_url = reverse_lazy('denetim')





#------------------------------------------------------

# tipi yaratma, güncelleme, silme ...

class TipiCreate(LoginRequiredMixin,CreateView):
    model = tipi
    fields = '__all__'
    success_url = "/islem/tipi/create/"

class TipiUpdate(LoginRequiredMixin,UpdateView):
    model = tipi
    fields = '__all__'
    success_url = "/islem/tipi/"

class TipiDelete(LoginRequiredMixin,DeleteView):
    model = tipi
    success_url = reverse_lazy('tipi')


#------------------------------------------------------

# zon yaratma, güncelleme, silme ...

class ZonCreate(LoginRequiredMixin,CreateView):
    model = zon
    fields = '__all__'
    success_url = "/islem/zon/create/"

class ZonUpdate(LoginRequiredMixin,UpdateView):
    model = zon
    fields = '__all__'
    success_url = "/islem/zon/"

class ZonDelete(LoginRequiredMixin,DeleteView):
    model = zon
    success_url = reverse_lazy('zon')





#-------------------------------------------------------------

# bolum yaratma, güncelleme, silme ...

class BolumCreate(LoginRequiredMixin,CreateView):
    model = bolum
    fields = '__all__'
    success_url = "/islem/bolum/create/"

class BolumUpdate(LoginRequiredMixin,UpdateView):
    model = bolum
    fields = '__all__'
    success_url = "/islem/bolum/"

class BolumDelete(LoginRequiredMixin,DeleteView):
    model = bolum
    success_url = reverse_lazy('bolum')



#------------------------------------------------------

# detay yaratma, güncelleme, silme ...

class DetayCreate(LoginRequiredMixin,CreateView):
    model = detay
    fields = '__all__'
    success_url = "/islem/detay/create/"

class DetayUpdate(LoginRequiredMixin,UpdateView):
    model = detay
    fields = '__all__'
    success_url = "/islem/detay/"

class DetayDelete(LoginRequiredMixin,DeleteView):
    model = detay
    success_url = reverse_lazy('detay')


#------------------------------------------------------

# proje_alanlari yaratma, güncelleme, silme ...

class ProjeAlanlariCreate(LoginRequiredMixin,CreateView):
    model = proje_alanlari
    fields = '__all__'
    success_url = "/islem/projealanlari/create/"

class ProjeAlanlariUpdate(LoginRequiredMixin,UpdateView):
    model = proje_alanlari
    fields = '__all__'
    success_url = "/islem/projealanlari/"

class ProjeAlanlariDelete(LoginRequiredMixin,DeleteView):
    model = proje_alanlari
    success_url = reverse_lazy('projealanlari')

#------------------------------------------------------

# yer yaratma, güncelleme, silme ...

class YerCreate(LoginRequiredMixin,CreateView):
    model = yer
    fields = '__all__'
    success_url = "/islem/yer/create/"

class YerUpdate(LoginRequiredMixin,UpdateView):
    model = yer
    fields = '__all__'
    success_url = "/islem/yer/"

class YerDelete(LoginRequiredMixin,DeleteView):
    model = yer
    success_url = reverse_lazy('yer')


#-------------------------------------------------------

# grup yaratma, güncelleme, silme ...

class GrupCreate(LoginRequiredMixin,CreateView):
    model = grup
    fields = '__all__'
    success_url = "/islem/grup/create/"

class GrupUpdate(LoginRequiredMixin,UpdateView):
    model = grup
    fields = '__all__'
    success_url = "/islem/grup/"

class GrupDelete(LoginRequiredMixin,DeleteView):
    model = grup
    success_url = reverse_lazy('grup')



#--------------------------------------------------------

# şirket yaratma, güncelleme, silme ...

class SirketCreate(LoginRequiredMixin,CreateView):
    model = sirket
    fields = '__all__'
    success_url = "/islem/sirket/create/"

class SirketUpdate(LoginRequiredMixin,UpdateView):
    model = sirket
    fields = '__all__'
    success_url = "/islem/sirket/"

class SirketDelete(LoginRequiredMixin,DeleteView):
    model = sirket
    success_url = reverse_lazy('sirket')



#-------------------------------------------------------

# Proje yaratma, güncelleme, silme ...

class ProjeCreate(LoginRequiredMixin,CreateView):
    model = proje
    fields = '__all__'
    success_url = "/islem/proje/create/"

class ProjeUpdate(LoginRequiredMixin,UpdateView):
    model = proje
    fields = '__all__'
    success_url = "/islem/proje/"

class ProjeDelete(LoginRequiredMixin,DeleteView):
    model = proje
    success_url = reverse_lazy('proje')


#-------------------------------------------------------

# qrdosyasi yaratma, güncelleme, silme ...

class QrdosyasiCreate(LoginRequiredMixin,CreateView):
    model = qrdosyasi
    fields = '__all__'
    success_url = "/islem/qrdosyasi/create/"

class QrdosyasiUpdate(LoginRequiredMixin,UpdateView):
    model = qrdosyasi
    fields = '__all__'
    success_url = "/islem/qrdosyasi/"

class QrdosyasiDelete(LoginRequiredMixin,DeleteView):
    model = qrdosyasi
    success_url = reverse_lazy('qrdosyasi')



#--------------------------------------------------------------


class SonucDetayUpdate(LoginRequiredMixin,UpdateView):
    model = sonuc_detay
    fields = '__all__'
    success_url = "/islem/sonuc/"


#-----------------------------------------?????????????????????????

class SonucDetayListView(LoginRequiredMixin,generic.ListView):
    model = sonuc_detay
    paginate_by = 20

class SonucDetayDetailView(LoginRequiredMixin,generic.DetailView):
    model = sonuc_detay


#------------------------------------------------------------

class TipiListView(LoginRequiredMixin,generic.ListView):
    model = tipi
    paginate_by = 20

class TipiDetailView(LoginRequiredMixin,generic.DetailView):
    model = tipi

#--------------------------------------------------------------

class ZonListView(LoginRequiredMixin,generic.ListView):
    model = zon
    paginate_by = 20

class ZonDetailView(LoginRequiredMixin,generic.DetailView):
    model = zon

#--------------------------------------------------------------


class BolumListView(LoginRequiredMixin,generic.ListView):
    model = bolum
    paginate_by = 20

class BolumDetailView(LoginRequiredMixin,generic.DetailView):
    model = bolum

#-----------------------------------------------------------

class DetayListView(LoginRequiredMixin,generic.ListView):
    model = detay
    paginate_by = 20

class DetayDetailView(LoginRequiredMixin,generic.DetailView):
    model = detay
#-----------------------------------------------------------

class ProjeAlanlariListView(LoginRequiredMixin,generic.ListView):
    model = proje_alanlari
    paginate_by = 20

class ProjeAlanlariDetailView(LoginRequiredMixin,generic.DetailView):
    model = proje_alanlari

#-----------------------------------------------------------

class YerListView(LoginRequiredMixin,generic.ListView):
    model = yer
    paginate_by = 20

class YerDetailView(LoginRequiredMixin,generic.DetailView):
    model = yer

#--------------------------------------------------------------

class GrupListView(LoginRequiredMixin,generic.ListView):
    model = grup
    paginate_by = 20

class GrupDetailView(LoginRequiredMixin,generic.DetailView):
    model = grup

#---------------------------------------------------------

class SirketListView(LoginRequiredMixin,generic.ListView):
    model = sirket
    paginate_by = 20

class SirketDetailView(LoginRequiredMixin,generic.DetailView):
    model = sirket


#---------------------------------------------------------

class QrdosyasiListView(LoginRequiredMixin,generic.ListView):
    model = qrdosyasi
    paginate_by = 20

class QrdosyasiDetailView(LoginRequiredMixin,generic.DetailView):
    model = qrdosyasi



#------------------------------------------------------------

class ProjeListView(LoginRequiredMixin,generic.ListView):
    model = proje
    paginate_by = 20

class ProjeDetailView(LoginRequiredMixin,generic.DetailView):
    model = proje

#------------------------------------------------------------

class DenetimListView(LoginRequiredMixin,generic.ListView):
    queryset = denetim.objects.filter(durum="A")
    paginate_by = 20

class DenetimDetailView(LoginRequiredMixin,generic.DetailView):
    queryset = denetim.objects.filter(durum="A")


#------------------------------------------------------------

class Denetim_2ListView(LoginRequiredMixin,generic.ListView):
    model = denetim
    queryset = denetim.objects.filter(durum="B")
    template_name = '/islem/denetim_isemrisonrasi_list.html'

class Denetim_2DetailView(LoginRequiredMixin,generic.DetailView):
    queryset = denetim.objects.filter(durum="B")

#------------------------------------------------------------

class Denetim_3ListView(LoginRequiredMixin,generic.ListView):
    #musteri = request.session.get('secili_musteri')
    queryset = denetim.objects.filter(durum="C")
    template_name = "/islem/denetim_sonlandirilan_list.html"

class Denetim_3DetailView(LoginRequiredMixin,generic.DetailView):
    queryset = denetim.objects.filter(durum="C")

#--------------------------------------------------------------




# -*- coding: utf-8 -*-
from .models import denetim
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.http import HttpResponse



# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.template import Context

@login_required
def generate_pdf(request):
    """Generate pdf."""
    # Model data
    denetim_obj = denetim.objects.all().order_by('denetim_adi')

    # Rendered
    html_string = render_to_string('pdf/weasyprint.html', {'denetim_obj': denetim_obj}).encode('utf-8')
    html = HTML(string=html_string)

    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'r')
        response.write(output.read())

    return response



#-------------------------------------------------------------------------------

from dal import autocomplete
from django.conf.urls import url
from .models import denetim


class denetimautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return denetim.objects.none()
        #qs = denetim.objects.all()
        qs = denetim.objects.order_by('id').exclude(durum="X").exclude(durum="Y")
        if self.q:
            qs = qs.filter(denetim_adi__icontains=self.q)
            print("qs filtre içinden", qs)
        return qs



class denetimrutinautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return denetim.objects.none()
        #qs = denetim.objects.all()
        qs = denetim.objects.filter(rutin_planli="R").filter(durum="A").filter(denetci=self.request.user.id)
        print("seçilen set denetim rutin autocomplete içinden...", qs)
        if self.q:
            qs = qs.filter(denetim_adi__icontains=self.q)
            print("qs filtre içinden", qs)
        return qs



class denolusturautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return denetim.objects.none()
        #qs = denetim.objects.all()
        #qs = denetim.objects.order_by('id').filter(durum="A").filter(yaratan=request.user)
        qs = denetim.objects.order_by('id').filter(durum="A")
        if self.q:
            qs = qs.filter(denetim_adi__icontains=self.q)
            print("qs filtre içinden", qs)
        return qs


class rutindenetimautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return denetim.objects.none()
        #qs = denetim.objects.all()
        #qs = denetim.objects.order_by('id').filter(durum="A").filter(yaratan=request.user)
        qs = denetim.objects.order_by('id').filter(rutin_planli="R")
        if self.q:
            qs = qs.filter(denetim_adi__icontains=self.q)
            print("qs filtre içinden", qs)
        return qs




@login_required
def deneme_denetim(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Denetim_Deneme_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            messages.success(request, 'Başarıyla oldu')
            return redirect('deneme_denetim')
        else:
            #messages.success(request, 'Formda uygunsuzluk var....')
            #return redirect('denetim_create')
            return render(request, 'islem/denetim_deneme_form.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        #selected_alt = request.session.get('selected_alt')
        form = Denetim_Deneme_Form()
        return render(request, 'islem/denetim_deneme_form.html', {'form': form,})



class sonucbolumautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return sonuc_bolum.objects.none()
        qs = sonuc_bolum.objects.all()

        denetim_deneme  = self.forwarded.get('denetim_deneme', None)
        print("denetim deneme...:", denetim_deneme)
        if denetim_deneme:
            qs = qs.filter(denetim=denetim_deneme)
        print("qs", qs)
        if self.q:
            qs = qs.filter(bolum__icontains=self.q)
        return qs

class sirketautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return sirket.objects.none()
        qs = sirket.objects.all()

        if self.q:
            qs = qs.filter(bolum__icontains=self.q)
        return qs



class sirketprojeautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return proje.objects.none()
        qs = proje.objects.all()

        sirket_proje  = self.forwarded.get('sirket', None)
        print("şirket proje...:", sirket)
        if sirket_proje:
            qs = qs.filter(sirket=sirket_proje)
        print("qs", qs)
        if self.q:
            qs = qs.filter(bolum__icontains=self.q)
        return qs





@login_required
def deneme_sonucbolum(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Ikili_Deneme_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            messages.success(request, 'Başarıyla oldu ')
            return redirect('deneme_sonucbolum')
        else:
            #messages.success(request, 'Formda uygunsuzluk var....')
            #return redirect('denetim_create')
            return render(request, 'islem/denetim_deneme_form_iki.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        #selected_alt = request.session.get('selected_alt')
        form = Ikili_Deneme_Form()
        return render(request, 'islem/denetim_deneme_form_iki.html', {'form': form,})

#------------------------------------------------------------------------------------

@login_required
def deneme_nebu(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NebuForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            messages.success(request, 'Başarıyla oldu ')
            return redirect('deneme_nebu')
        else:
            #messages.success(request, 'Formda uygunsuzluk var....')
            #return redirect('denetim_create')
            return render(request, 'islem/denetim_deneme_nebu.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        #selected_alt = request.session.get('selected_alt')
        form = NebuForm()
        return render(request, 'islem/denetim_deneme_nebu.html', {'form': form,})

#---------------------------------response.json()--------------------------------------------------------

class takipciautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
            #return sonuc_bolum.objects.none()

        #qs = Profile.objects.filter(denetim_takipcisi="E")
        qs = User.objects.all().order_by('id')
        print("null olmasın şimdi...:", qs)
        if self.q:
            qs = qs.filter(user__username__icontains=self.q)
        return qs


class bolumautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return bolum.objects.none()
        #bolum_tipi = request.session.get('bolum_tipi')
        bolum_tipi  = self.forwarded.get('tipi', None)
        print("bolüm tipi...", bolum_tipi)
        #qs = bolum.objects.all()
        qs = bolum.objects.none()
        if bolum_tipi:
            zon_obj = zon.objects.filter(tipi=bolum_tipi).order_by('tipi')
            for zonlar in zon_obj:
                print("zonlar id..", zonlar.id)
                # burada çözmek lazım....
                qx = bolum.objects.filter(zon=zonlar.id).order_by('zon').exclude(detay__bolum=None)
                print("qx...", qx)
                qs = qs.union(qx)
        print("qs filtre öncesi..", qs)

        if self.q:
            qs = qs.filter(bolum_adi__icontains=self.q)
        return qs


class detayautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return detay.objects.none()
        qs = detay.objects.all().order_by('id')
        if self.q:
            qs = qs.filter(detay_adi__icontains=self.q)
        return qs


class spvautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return detay.objects.none()
        kullanici = self.request.user
        sirket = kullanici.profile.sirket
        spvler_obj = Profile.objects.filter(denetim_grup_yetkilisi="E")

        serbest_spv_list = []
        for spv in spvler_obj:
            if spv.sirket.turu == "D":
                usr_obj = spv.user
                serbest_spv_list.append(usr_obj)

        spv_obj = spv_yetkilisi.objects.filter(sirket=sirket)
        grupdisi_list = []
        for spv in spv_obj:
            kisi = spv.spv_yetkilisi.id
            kisi_obj = User.objects.get(id=kisi)
            print("kişi object...", kisi_obj)
            kisi_sirket = kisi_obj.profile.sirket
            print("kişi şirket..", kisi_sirket)
            if kisi_sirket:
                if kisi_sirket.turu == "D":
                    grupdisi_list.append(kisi_obj)

        kalan_list = list(set(serbest_spv_list) - set(grupdisi_list))

        id_s = []
        for x in kalan_list:
            id_s.append(x.id)
        print("işte id ler...", id_s)
        ser_spv_obj = User.objects.filter(pk__in=id_s)
        print("seçili liste sonunda...", ser_spv_obj)
        return ser_spv_obj

    def get_result_label(self, item):
        str1 = str(item.get_full_name())
        str2 = str(item.profile.sirket)
        send_str = str1 + " - " + str2
        return send_str



class denautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return detay.objects.none()
        kullanici = self.request.user
        sirket = kullanici.profile.sirket
        denler_obj = Profile.objects.filter(denetci="E")

        serbest_den_list = []
        for den in denler_obj:
            if den.sirket.turu == "D":
                usr_obj = den.user
                serbest_den_list.append(usr_obj)

        den_obj = den_yetkilisi.objects.filter(sirket=sirket)
        grupdisi_list = []
        for den in den_obj:
            kisi = den.den_yetkilisi.id
            kisi_obj = User.objects.get(id=kisi)
            print("kişi object...", kisi_obj)
            kisi_sirket = kisi_obj.profile.sirket
            print("kişi şirket..", kisi_sirket)
            if kisi_sirket:
                if kisi_sirket.turu == "D":
                    grupdisi_list.append(kisi_obj)

        kalan_list = list(set(serbest_den_list) - set(grupdisi_list))

        id_s = []
        for x in kalan_list:
            id_s.append(x.id)
        print("işte id ler...", id_s)
        ser_den_obj = User.objects.filter(pk__in=id_s)
        print("seçili liste sonunda...", ser_den_obj)
        return ser_den_obj

    def get_result_label(self, item):
        str1 = str(item.get_full_name())
        str2 = str(item.profile.sirket)
        send_str = str1 + " - " + str2
        return send_str




class tipiautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return tipi.objects.none()
        qs = tipi.objects.all().order_by('tipi_adi')
        if self.q:
            qs = qs.filter(tipi_adi__icontains=self.q)
        return qs

class zonautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return zon.objects.none()
        qs = zon.objects.all().order_by('zon_adi')
        if self.q:
            qs = qs.filter(zon_adi__icontains=self.q)
        return qs

class sirket2autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return proje.objects.none()
        qs = sirket.objects.all().order_by('sirket_adi')
        if self.q:
            qs = qs.filter(sirket_adi__icontains=self.q)
        return qs


class projeautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return proje.objects.none()
        qs = proje.objects.all().order_by('proje_adi')
        if self.q:
            qs = qs.filter(proje_adi__icontains=self.q)
        return qs

class denetciautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return user.objects.none()
        qs = Profile.objects.filter(denetci="E").order_by('user')
        if self.q:
            qs = qs.filter(user__username__icontains=self.q)
        return qs


class list_tipiautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return user.objects.none()
        qs = tipi.objects.all()
        return qs


class list_zonautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return user.objects.none()
        tipi = self.forwarded.get('tipi', None)
        print("tipi...", tipi)

        if not tipi:
            qs = None
        else:
            qs = zon.objects.filter(tipi=tipi)

        return qs




class list_bolumautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return user.objects.none()
        zon = self.forwarded.get('zon', None)
        print("zon...", zon)

        if not zon:
            qs = None
        else:
            qs = bolum.objects.filter(zon=zon)

        return qs


@login_required
def bildirim(request):
    print("bildirime geldik.")
    response_data ={}
    if request.method == 'GET':
        selected = request.GET.get('selected', None)
        print("js bildirim içinden zaman...", datetime.datetime.now())
        response_data = ""
        proje = request.user.profile.proje
        kisi = request.user
        print("proje", proje)
        if proje == None:
            pass
        else:
            bugun = datetime.datetime.now()
            yedigun = datetime.timedelta(14,0,0)
            yedigun_once = bugun - yedigun
            print("yedi gün önce...", yedigun_once)
            n = Notification.objects.filter(viewed=False).filter(kisi=kisi).filter(timestamp__gt=yedigun_once).values()
            #print("obje - dictionary...",n)
            if n:
                n_list = list(n)
                for i in n_list:
                    i['timestamp'] = str(i['timestamp'])

                #print("liste hali...", n_list)
                response_data = {"response_data" : n_list}
                #print("response  data...", response_data)
                response_data = json.dumps(n_list)

        return HttpResponse(response_data, content_type='application/json')


def popup_notif(request):
        n_list = Notification.objects.filter(viewed=False).values()
        print("obje...",n_list)
        return render(request, 'popup_notif.html', {'n_list': n_list})


def dosyalari_duzenle(request):
        print("dosyaları düzenleye kadar geldi.....")
        return render(request, 'islem/dosyalari_duzenle.html',)


def dosyalari_duzenle_kesin(request):
    dosya = "dosyalar düzenlenecek..."
    # memnuniyet .....
    mem_obj = Memnuniyet.objects.all()
    mem_count_var = 0
    mem_count_sil = 0
    for mem in mem_obj:
        mac_no_a = mem.mac_no
        tipi_a = mem.tipi
        yer_a = mem.yer.id
        oy_a = mem.oy
        sebep_a = mem.sebep
        gelen_tarih_a = mem.gelen_tarih
        timestamp_a = mem.timestamp

        yer_obj = yer.objects.filter(mac_no=mac_no_a).first()
        if yer_obj:
            alan_obj = proje_alanlari.objects.filter(yer=yer_obj.id).first()
            proje_obj = proje.objects.filter(proje_alanlari=alan_obj.id).first()

            kaydetme_obj = Memnuniyet(  proje_id=proje_obj.id,
                                        p_alani_id=alan_obj.id,
                                        mac_no = mac_no_a,
                                        tipi = tipi_a,
                                        yer_id = yer_a,
                                        oy = oy_a,
                                        sebep = sebep_a,
                                        gelen_tarih = gelen_tarih_a,
                                        timestamp = timestamp_a,)
            kaydetme_obj.save()
            mem_count_var = mem_count_var + 1
        else:
            mem.delete()
            mem_count_sil = mem_count_sil + 1



    #operasyon .....
    opr_obj = Operasyon_Data.objects.all()
    opr_count_var = 0
    opr_count_sil = 0
    for opr in opr_obj:
        mac_no_a = opr.mac_no
        tipi_a = opr.tipi
        yer_a = opr.yer.id
        rfid_no_a = opr.rfid_no
        bas_tarih_a = opr.bas_tarih
        son_tarih_a = opr.son_tarih
        bild_tipi_a = opr.bild_tipi
        timestamp_a = opr.timeStamp
        yer_obj = yer.objects.filter(mac_no=mac_no_a).first()
        if yer_obj:
            alan_obj = proje_alanlari.objects.filter(yer=yer_obj.id).first()
            proje_obj = proje.objects.filter(proje_alanlari=alan_obj.id).first()
            kaydetme_obj = Operasyon_Data(  proje_id=proje_obj.id,
                                            p_alani_id=alan_obj.id,
                                            mac_no = mac_no_a,
                                            tipi = tipi_a,
                                            yer_id = yer_a,
                                            rfid_no = oy_a,
                                            bas_tarih = bas_tarih_a,
                                            son_tarih = son_tarih_a,
                                            timestamp = timestamp_a,)
            kaydetme_obj.save()
            opr_count_var = opr_count_var + 1
        else:
            opr.delete()
            opr_count_sil = opr_count_sil + 1


    #denetim .....
    den_obj = Denetim_Data.objects.all()
    den_count_var = 0
    den_count_sil = 0
    for den in den_obj:
        mac_no_a = den.mac_no
        tipi_a = den.tipi
        yer_a = den.yer.id
        rfid_no_a = den.rfid_no
        kod_a = den.kod
        gelen_tarih_a = den.gelen_tarih
        timestamp_a = den.timestamp
        yer_obj = yer.objects.filter(mac_no=mac_no_a).first()
        if yer_obj:
            alan_obj = proje_alanlari.objects.filter(yer=yer_obj.id).first()
            proje_obj = proje.objects.filter(proje_alanlari=alan_obj.id).first()
            kaydetme_obj = Denetim_Data(  proje_id=proje_obj.id,
                                        p_alani_id=alan_obj.id,
                                        mac_no = mac_no_a,
                                        tipi = tipi_a,
                                        yer_id = yer_a,
                                        kod = kod_a,
                                        rfid_no = rfid_no_a,
                                        gelen_tarih = gelen_tarih_a,
                                        timestamp = timestamp_a,)
            kaydetme_obj.save()
            den_count_var = den_count_var + 1
        else:
            den.delete()
            den_count_sil = den_count_sil + 1


    #sayı....
    say_obj = Sayi_Data.objects.all()
    say_count_var = 0
    say_count_sil = 0
    for say in say_obj:
        mac_no_a = say.mac_no
        tipi_a = say.tipi
        yer_a = say.yer.id
        adet_a = say.adet
        gelen_tarih_a = say.gelen_tarih
        timestamp_a = say.timestamp
        yer_obj = yer.objects.filter(mac_no=mac_no_a).first()
        if yer_obj:
            alan_obj = proje_alanlari.objects.filter(yer=yer_obj.id).first()
            proje_obj = proje.objects.filter(proje_alanlari=alan_obj.id).first()
            kaydetme_obj = Sayi_Data(   proje_id=proje_obj.id,
                                        p_alani_id=alan_obj.id,
                                        mac_no = mac_no_a,
                                        tipi = tipi_a,
                                        yer_id = yer_a,
                                        adet = adet_a,
                                        gelen_tarih = gelen_tarih_a,
                                        timestamp = timestamp_a,)
            kaydetme_obj.save()
            say_count_var = say_count_var + 1
        else:
            say.delete()
            say_count_sil = say_count_sil + 1


    context = { 'mem_count_var': mem_count_var, 'mem_count_sil': mem_count_sil,
                'den_count_var': den_count_var, 'den_count_sil': den_count_sil,
                'opr_count_var': opr_count_var, 'opr_count_sil': opr_count_sil,
                'say_count_var': say_count_var, 'say_count_sil': say_count_sil,
                }


    return render(request, 'islem/dosyalari_duzenle_kesin.html', context)



from islem.services  import get_memnuniyet_list, get_rfid_list, proje_varmi_kontrol, sirket_varmi_kontrol, index_hazirla_proje
from islem.services  import get_operasyon_list, get_denetim_saha_list, get_ariza_list, get_yerud_list, get_sy_list
from islem.services import get_m_list, get_o_list, get_d_list, get_a_list, admin_kontrol, get_sms, rapor_verisi_hazirla
from islem.services import oran_memnuniyet, ana_menu_mky_hazirla, mem_veri_hazirla



#----------------------------------------------------------------------------------------
from dateutil import parser
@login_required
def memnuniyet_list(request, pk=None):
    user = request.user
    test_url = str(request.get_full_path)
    print("işte deneme url si.....", test_url)
    src_str = '?page'
    deger = test_url.find(src_str)
    if deger == -1:
        ilk_arama = True
    else:
        ilk_arama = False

    print("değer ....", deger)
    print("ilk_arama", ilk_arama)



    if proje_varmi_kontrol(request):
        print("proje var mı kontrolden geçtik.....")
        proje = user.profile.proje
        m2_list = request.session.get('rs_m_list')

        if not (m2_list) or ilk_arama:
            m_list = get_m_list(request)
            rs_m_list = []
            for x in m_list:
                temp = {}
                temp['yer'] = x['yer']
                temp['aciklama'] = x['aciklama']
                temp['deger'] = x['deger']
                temp['proje'] = x['proje']
                temp['gelen_tarih'] = str(x['gelen_tarih'])
                rs_m_list.append(temp)
            request.session['rs_m_list'] = rs_m_list
        else:
            rs_okuma = True
            print(" rs okuma....", rs_okuma)
            m_list = []
            for x in m2_list:
                temp = {}
                temp['gelen_tarih'] = parser.parse(x['gelen_tarih'])
                temp['yer'] = x['yer']
                temp['aciklama'] = x['aciklama']
                temp['deger'] = x['deger']
                temp['proje'] = x['proje']
                m_list.append(temp)

        paginator = Paginator(m_list, 25)
        page = request.GET.get('page')

        try:
            n = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            n = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            n = paginator.page(paginator.num_pages)

        print("işte sayfalanmış liste...", n)
        return render(request, 'islem/memnuniyet_list.html', {'memnuniyet_list': n,})

    else:
        print("buraya geldi...proje yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})


@login_required
def memnuniyet_create(request, pk=None):
    t_stamp = str(datetime.datetime.now())
    tipi = "1"
    proje = "1"
    p_alani = "1"
    yer = "1"
    oy = "1"
    sebep = "6"
    print("okunan zaman......menuniyet create.............", t_stamp)
    response = requests.post("http://"+settings.ADR_LOCAL+"/ws/memnuniyet_list/",
        json={"mac_no":123451234512345, "tipi": tipi, "proje": proje, "p_alani": p_alani , "yer": yer, "oy": oy, "sebep": sebep, "gelen_tarih": t_stamp, "timestamp": t_stamp }, auth=(settings.USER_GLB, settings.PASW_GLB))
    response.json()
    print("status code..", response.status_code)
    return redirect('memnuniyet_list')



@login_required
def mk_memnuniyet_list(request):
    user = request.user
    if sirket_varmi_kontrol(request):
        print("şirket var mı kontrolden geçtik.....")
        sirket = user.profile.sirket
        if request.method == "POST":
            form = SirketIcinProjeForm(request.POST, sirket=sirket)
            if form.is_valid():
                proje = request.POST.get('proje', "")
                print(" proje form okunduktan sonra post...", proje)

                m_list = request.session.get('mk_m_list')
                mk_proje = request.session.get('mk_m_proje')

                if mk_proje == proje:

                    m2_list = []
                    for x in m_list:
                        temp = {}

                        temp['gelen_tarih'] = parser.parse(x['gelen_tarih'])
                        temp['yer'] = x['yer']
                        temp['aciklama'] = x['aciklama']
                        temp['deger'] = x['deger']
                        temp['proje'] = x['proje']
                        m2_list.append(temp)

                else:
                    bugun = datetime.datetime.now()
                    yedigun = datetime.timedelta(7,0,0)
                    yedigun_once = bugun - yedigun
                    memnuniyet_obj = Memnuniyet.objects.filter(proje=proje).filter(gelen_tarih__gt=yedigun_once).order_by("-id")
                    m_list = []
                    m2_list = []
                    for x in memnuniyet_obj:
                        temp = {}
                        temp2 = {}

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

                        #proje_no = x.proje
                        #proje_obj = proje.objects.get(id=proje_no)
                        #if proje_obj:
                        temp['proje'] = x.proje.proje_adi
                        #else:
                        #    temp['proje'] = proje

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

                        temp2['gelen_tarih'] = parser.parse(temp['gelen_tarih'])
                        temp2['yer'] = temp['yer']
                        temp2['aciklama'] = temp['aciklama']
                        temp2['deger'] = temp['deger']
                        temp2['proje'] = temp['proje']
                        m2_list.append(temp2)


                    request.session['mk_m_list'] = m_list
                    request.session['mk_m_proje'] = proje


                paginator = Paginator(m2_list, 25)
                page = request.GET.get('page')
                try:
                    n = paginator.page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    n = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    n = paginator.page(paginator.num_pages)
                print("işte sayfalanmış liste...", n)

                return render(request, 'islem/mk_memnuniyet_list.html', {'form': form, 'mk_memnuniyet_list': n})
            else:
                print("form is invalid.....")
                return redirect('mk_memnuniyet_list')
        else:
            m_list = request.session.get('mk_m_list')
            mk_proje = request.session.get('mk_m_proje')
            print("işte alması gereken m list..!!!!!!!!!!!!!!!!!!!!!!!!", m_list)
            m2_list = []
            if m_list:
                for x in m_list:
                    temp = {}
                    temp['gelen_tarih'] = parser.parse(x['gelen_tarih'])
                    temp['yer'] = x['yer']
                    temp['aciklama'] = x['aciklama']
                    temp['deger'] = x['deger']
                    temp['proje'] = x['proje']
                    m2_list.append(temp)
                print("işte alması gereken m2 list..!!!!!!!!!!!!!!!!!!!!!!!!", m2_list)
            paginator = Paginator(m2_list, 25)
            page = request.GET.get('page')
            try:
                n = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                n = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                n = paginator.page(paginator.num_pages)

            form = SirketIcinProjeForm(sirket=sirket)
            form.fields["proje"].initial = mk_proje
            print("get içinde mi.....")
            #n = ""
            return render(request, 'islem/mk_memnuniyet_list.html', {'form': form, 'mk_memnuniyet_list': n})

    else:
        print("buraya geldi...şirket merkez yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})






#----------------------------------------------------------------------------------------------
from django.core.serializers.json import DjangoJSONEncoder

@login_required
def operasyon_list(request, pk=None):

    user = request.user
    test_url = str(request.get_full_path)
    print("işte deneme url si.....", test_url)
    src_str = '?page'
    deger = test_url.find(src_str)
    if deger == -1:
        ilk_arama = True
    else:
        ilk_arama = False
    print("değer ....", deger)
    print("ilk_arama", ilk_arama)



    if proje_varmi_kontrol(request):
        print("proje var mı kontrolden geçtik.....")
        proje = user.profile.proje
        print("atanmış proje var...")
        o2_list = request.session.get('rs_o_list')

        if not(o2_list) or ilk_arama:
            print("ilk bölüm...")
            o_list = get_o_list(request)
            print("get o listten gelen o list...", o_list)
            rs_o_list = []
            for x in o_list:
                temp = {}
                temp['bas_tarih'] = str(x['bas_tarih'])
                temp['son_tarih'] = str(x['son_tarih'])
                temp['sure'] = None
                temp['yer'] = x['yer']
                temp['adi'] = x['adi']
                temp['soyadi'] = x['soyadi']
                temp['deger'] = x['deger']
                temp['proje'] = x['proje']
                rs_o_list.append(temp)
            request.session['rs_o_list'] = rs_o_list
            print("if sonrasından gelen o list....", o_list)
        else:
            print("ikinci bölüm...")
            o_list = []
            for x in o2_list:
                temp = {}
                temp['bas_tarih'] = parser.parse(x['bas_tarih'])
                temp['son_tarih'] = parser.parse(x['son_tarih'])
                temp['sure'] = temp['son_tarih'] - temp['bas_tarih']
                temp['yer'] = x['yer']
                temp['adi'] = x['adi']
                temp['soyadi'] = x['soyadi']
                temp['deger'] = x['deger']
                temp['proje'] = x['proje']
                o_list.append(temp)

        print("paginator a göndermeden önce o list...", o_list)

        paginator = Paginator(o_list, 25)
        page = request.GET.get('page')
        try:
            n = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            n = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            n = paginator.page(paginator.num_pages)


        print("template göndermeden önce o list...", o_list)

        return render(request, 'islem/operasyon_list.html', {'operasyon_list': n})

    else:
        print("buraya geldi...proje yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})


@login_required
def operasyon_create(request, pk=None):
    t_stamp = str(datetime.datetime.now())
    bas_tarih = str(datetime.datetime(2018, 10, 15, 13, 9, 45))
    tipi = "1"
    proje = "1"
    p_alani = "1"
    yer = "1"
    rfid_no = "21414016072178"
    bild_tipi = "M"
    print("okunan zaman......operasyon create.............", t_stamp)
    response = requests.post("http://"+settings.ADR_LOCAL+"/ws/operasyon_list/",
        json={"mac_no":123451234512345, "tipi": tipi, "proje": proje, "p_alani": p_alani , "yer": yer, "rfid_no": rfid_no, "bas_tarih": bas_tarih, "son_tarih": t_stamp, "bild_tipi": bild_tipi, "timestamp": t_stamp }, auth=(settings.USER_GLB, settings.PASW_GLB))
    response.json()
    print("status code..", response.status_code)
    return redirect('operasyon_list')






@login_required
def mk_operasyon_list(request):
    user = request.user
    if sirket_varmi_kontrol(request):
        print("şirket var mı kontrolden geçtik.....")
        sirket = user.profile.sirket
        if request.method == "POST":
            form = SirketIcinProjeForm(request.POST, sirket=sirket)
            if form.is_valid():
                proje = request.POST.get('proje', "")
                print(" proje form okunduktan sonra post...", proje)

                o_list = request.session.get('mk_o_list')
                mk_proje = request.session.get('mk_o_proje')

                if mk_proje == proje:
                    o2_list = []
                    for x in o_list:
                        temp = {}
                        temp['son_tarih'] = parser.parse(x['son_tarih'])
                        temp['bas_tarih'] = parser.parse(x['bas_tarih'])
                        temp['sure'] = temp['son_tarih'] - temp['bas_tarih']
                        temp['adi'] = x['adi']
                        temp['soyadi'] = x['soyadi']
                        temp['deger'] = x['deger']
                        temp['proje'] = x['proje']
                        temp['yer'] = x['yer']
                        o2_list.append(temp)

                else:
                    bugun = datetime.datetime.now()
                    yedigun = datetime.timedelta(7,0,0)
                    yedigun_once = bugun - yedigun
                    operasyon_obj = Operasyon_Data.objects.filter(proje=proje).filter(bas_tarih__gt=yedigun_once).order_by("-id")
                    o_list = []
                    o2_list = []
                    for x in operasyon_obj:
                        temp = {}
                        temp2 = {}
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

                        temp['sure'] = x.son_tarih - x.bas_tarih
                        print("süre....", temp['sure'])

                        if x.bild_tipi == "A":
                            temp['deger'] = 0
                        else:
                            temp['deger'] = None

                        temp2['son_tarih'] = str(temp['son_tarih'])
                        temp2['bas_tarih'] = str(temp['bas_tarih'])
                        temp2['sure'] = None
                        temp2['adi'] = temp['adi']
                        temp2['soyadi'] = temp['soyadi']
                        temp2['deger'] = temp['deger']
                        temp2['proje'] = temp['proje']
                        temp2['yer'] = temp['yer']
                        o2_list.append(temp)
                        o_list.append(temp2)


                    request.session['mk_o_list'] = o_list
                    request.session['mk_o_proje'] = proje


                paginator = Paginator(o2_list, 25)
                page = request.GET.get('page')
                try:
                    n = paginator.page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    n = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    n = paginator.page(paginator.num_pages)
                print("işte sayfalanmış liste...", n)

                return render(request, 'islem/mk_operasyon_list.html', {'form': form, 'mk_operasyon_list': n})
            else:
                print("form is invalid.....")
                return redirect('mk_operasyon_list')
        else:
            o_list = request.session.get('mk_o_list')
            mk_proje = request.session.get('mk_o_proje')
            print("işte alması gereken m list..!!!!!!!!!!!!!!!!!!!!!!!!", o_list)
            o2_list = []
            if o_list:
                for x in o_list:
                    temp = {}
                    temp['son_tarih'] = parser.parse(x['son_tarih'])
                    temp['bas_tarih'] = parser.parse(x['bas_tarih'])
                    temp['sure'] = temp['son_tarih'] - temp['bas_tarih']
                    temp['adi'] = x['adi']
                    temp['soyadi'] = x['soyadi']
                    temp['deger'] = x['deger']
                    temp['proje'] = x['proje']
                    temp['yer'] = x['yer']
                    o2_list.append(temp)
                #print("işte alması gereken m2 list..!!!!!!!!!!!!!!!!!!!!!!!!", m2_list)
            paginator = Paginator(o2_list, 25)
            page = request.GET.get('page')
            try:
                n = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                n = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                n = paginator.page(paginator.num_pages)

            form = SirketIcinProjeForm(sirket=sirket)
            form.fields["proje"].initial = mk_proje
            print("get içinde mi.....")
            #n = ""
            return render(request, 'islem/mk_operasyon_list.html', {'form': form, 'mk_operasyon_list': n})

    else:
        print("buraya geldi...şirket merkez yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})












#-----------------------------------------------------------------------------------------------


@login_required
def den_saha_list(request, pk=None):
    user = request.user
    test_url = str(request.get_full_path)
    print("işte deneme url si.....", test_url)
    src_str = '?page'
    deger = test_url.find(src_str)
    if deger == -1:
        ilk_arama = True
    else:
        ilk_arama = False

    print("değer ....", deger)
    print("ilk_arama", ilk_arama)

    if proje_varmi_kontrol(request):
        print("proje var mı kontrolden geçtik.....")
        proje = user.profile.proje
        d2_list = request.session.get('rs_d_list')

        if not (d2_list) or ilk_arama:
            d_list = get_d_list(request)
            rs_d_list = []
            for x in d_list:
                temp = {}
                temp['yer'] = x['yer']
                temp['aciklama'] = x['aciklama']
                temp['deger'] = x['deger']
                temp['proje'] = x['proje']
                temp['gelen_tarih'] = str(x['gelen_tarih'])
                temp['adi'] = x['adi']
                temp['soyadi'] = x['soyadi']
                rs_d_list.append(temp)
            request.session['rs_d_list'] = rs_d_list
        else:
            rs_okuma = True
            print(" rs okuma....", rs_okuma)
            d_list = []
            for x in d2_list:
                temp = {}
                temp['gelen_tarih'] = parser.parse(x['gelen_tarih'])
                temp['yer'] = x['yer']
                temp['aciklama'] = x['aciklama']
                temp['deger'] = x['deger']
                temp['proje'] = x['proje']
                temp['adi'] = x['adi']
                temp['soyadi'] = x['soyadi']
                d_list.append(temp)

        paginator = Paginator(d_list, 25)
        page = request.GET.get('page')

        try:
            n = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            n = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            n = paginator.page(paginator.num_pages)

        print("işte sayfalanmış liste...", n)
        return render(request, 'islem/denetim_saha_list.html', {'denetim_saha_list': n,})

    else:
        print("buraya geldi...proje yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})









@login_required
def den_saha_create(request, pk=None):
    t_stamp = str(datetime.datetime.now())
    tipi = "1"
    proje = "1"
    p_alani = "1"
    yer = "1"
    rfid_no = "1741053721759"
    kod = "3"
    print("okunan zaman......denetim create.............", t_stamp)
    response = requests.post("http://"+settings.ADR_LOCAL+"/ws/denetim_list/",
        json={"mac_no":123451234512345, "tipi": tipi, "proje": proje, "p_alani": p_alani, "yer": yer, "rfid_no": rfid_no, "kod": kod, "gelen_tarih": t_stamp, "timestamp": t_stamp }, auth=(settings.USER_GLB, settings.PASW_GLB))
    response.json()
    print("status code..", response.status_code)
    return redirect('den_saha_list')



@login_required
def mk_den_saha_list(request):
    user = request.user
    if sirket_varmi_kontrol(request):
        print("şirket var mı kontrolden geçtik.....")
        sirket = user.profile.sirket
        if request.method == "POST":
            form = SirketIcinProjeForm(request.POST, sirket=sirket)
            if form.is_valid():
                proje = request.POST.get('proje', "")
                print(" proje form okunduktan sonra post...", proje)

                d_list = request.session.get('mk_d_list')
                mk_proje = request.session.get('mk_d_proje')

                if mk_proje == proje:
                    d2_list = []
                    for x in d_list:
                        temp = {}
                        temp['gelen_tarih'] = parser.parse(x['gelen_tarih'])
                        temp['aciklama'] = x['aciklama']
                        temp['adi'] = x['adi']
                        temp['soyadi'] = x['soyadi']
                        temp['deger'] = x['deger']
                        temp['proje'] = x['proje']
                        temp['yer'] = x['yer']
                        d2_list.append(temp)

                else:
                    bugun = datetime.datetime.now()
                    yedigun = datetime.timedelta(7,0,0)
                    yedigun_once = bugun - yedigun
                    denetim_obj = Denetim_Data.objects.filter(proje=proje).filter(gelen_tarih__gt=yedigun_once).order_by("-id")
                    d_list = []
                    d2_list = []
                    for x in denetim_obj:
                        temp = {}
                        temp2 = {}
                        gelen_tarih = x.gelen_tarih
                        temp['gelen_tarih'] = gelen_tarih
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

                        sayi = int(x.kod)

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


                        temp2['gelen_tarih'] = str(temp['gelen_tarih'])
                        temp2['aciklama'] = temp['aciklama']
                        temp2['adi'] = temp['adi']
                        temp2['soyadi'] = temp['soyadi']
                        temp2['deger'] = temp['deger']
                        temp2['proje'] = temp['proje']
                        temp2['yer'] = temp['yer']
                        d2_list.append(temp)
                        d_list.append(temp2)


                    request.session['mk_d_list'] = d_list
                    request.session['mk_d_proje'] = proje


                paginator = Paginator(d2_list, 25)
                page = request.GET.get('page')
                try:
                    n = paginator.page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    n = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    n = paginator.page(paginator.num_pages)
                print("işte sayfalanmış liste...", n)

                return render(request, 'islem/mk_den_saha_list.html', {'form': form, 'mk_den_saha_list': n})
            else:
                print("form is invalid.....")
                return redirect('mk_den_saha_list')
        else:
            d_list = request.session.get('mk_d_list')
            mk_proje = request.session.get('mk_d_proje')
            d2_list = []
            if d_list:
                for x in d_list:
                    temp = {}
                    temp['gelen_tarih'] = parser.parse(x['gelen_tarih'])
                    temp['aciklama'] = x['aciklama']
                    temp['adi'] = x['adi']
                    temp['soyadi'] = x['soyadi']
                    temp['deger'] = x['deger']
                    temp['proje'] = x['proje']
                    temp['yer'] = x['yer']
                    d2_list.append(temp)
            paginator = Paginator(d2_list, 25)
            page = request.GET.get('page')
            try:
                n = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                n = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                n = paginator.page(paginator.num_pages)

            form = SirketIcinProjeForm(sirket=sirket)
            form.fields["proje"].initial = mk_proje
            return render(request, 'islem/mk_den_saha_list.html', {'form': form, 'mk_den_saha_list': n})

    else:
        print("buraya geldi...şirket merkez yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})




@login_required
def mk_projealanlari_listele(request):
    user = request.user
    if sirket_varmi_kontrol(request):
        print("şirket var mı kontrolden geçtik.....")
        sirket = user.profile.sirket
        if request.method == "POST":
            form = SirketIcinProjeForm(request.POST, sirket=sirket)
            if form.is_valid():
                proje = request.POST.get('proje', "")
                print(" proje form okunduktan sonra post...", proje)
                pa_obj = proje_alanlari.objects.filter(proje=proje)
                return render(request, 'islem/mk_pa_list.html', {'form': form, 'mk_pa_list': pa_obj, 'proje': proje})
            else:
                print("form is invalid.....")
                return redirect('mk_projealanlari_listele')
        else:

            form = SirketIcinProjeForm(sirket=sirket)
            n = None
            proje = None
            return render(request, 'islem/mk_pa_list.html', {'form': form, 'mk_pa_list': n, 'proje': proje})

    else:
        print("buraya geldi...şirket merkez yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})


@login_required
def mk_yer_listele(request):
    user = request.user
    if sirket_varmi_kontrol(request):
        print("şirket var mı kontrolden geçtik.....")
        sirket = user.profile.sirket
        if request.method == "POST":
            form = SirketIcinProjeForm(request.POST, sirket=sirket)
            if form.is_valid():
                proje = request.POST.get('proje', "")
                print(" proje form okunduktan sonra post...", proje)
                qs = yer.objects.none()
                pa_obj = proje_alanlari.objects.filter(proje=proje)
                for x in pa_obj:
                    qx = yer.objects.filter(proje_alanlari=x.id)
                    qs = qs.union(qx)
                qs = qs.order_by('id')
                return render(request, 'islem/mk_yer_list.html', {'form': form, 'mk_yer_list': qs, 'proje': proje})
            else:
                print("form is invalid.....")
                return redirect('mk_yer_listele')
        else:

            form = SirketIcinProjeForm(sirket=sirket)
            n = None
            proje = None
            return render(request, 'islem/mk_yer_list.html', {'form': form, 'mk_yer_list': n, 'proje': proje})

    else:
        print("buraya geldi...şirket merkez yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})


@login_required
def mk_rfid_listele(request):
    user = request.user
    if sirket_varmi_kontrol(request):
        print("şirket var mı kontrolden geçtik.....")
        sirket = user.profile.sirket
        if request.method == "POST":
            form = SirketIcinProjeForm(request.POST, sirket=sirket)
            if form.is_valid():
                proje = request.POST.get('proje', "")
                print(" proje form okunduktan sonra post...", proje)
                rfid_obj = rfid_dosyasi.objects.filter(proje=proje)
                return render(request, 'islem/mk_rfid_list.html', {'form': form, 'mk_rfid_list': rfid_obj, 'proje': proje})
            else:
                print("form is invalid.....")
                return redirect('mk_rfid_listele')
        else:

            form = SirketIcinProjeForm(sirket=sirket)
            n = None
            proje = None
            return render(request, 'islem/mk_rfid_list.html', {'form': form, 'mk_rfid_list': n, 'proje': proje})

    else:
        print("buraya geldi...şirket merkez yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})




#--------------------------------------------------------------------------------------------------

@login_required
def ariza_list(request, pk=None):
    user = request.user
    test_url = str(request.get_full_path)
    print("işte deneme url si.....", test_url)
    src_str = '?page'
    deger = test_url.find(src_str)
    if deger == -1:
        ilk_arama = True
    else:
        ilk_arama = False

    print("değer ....", deger)
    print("ilk_arama", ilk_arama)

    if proje_varmi_kontrol(request):
        print("proje var mı kontrolden geçtik.....")
        proje = user.profile.proje
        a2_list = request.session.get('rs_a_list')

        if not (a2_list) or ilk_arama:
            a_list = get_a_list(request)
            rs_a_list = []
            for x in a_list:
                temp = {}
                temp['yer'] = x['yer']
                temp['aciklama'] = x['aciklama']
                temp['proje'] = x['proje']
                temp['gelen_tarih'] = str(x['gelen_tarih'])
                temp['adi'] = x['adi']
                temp['soyadi'] = x['soyadi']
                temp['progress'] = x['progress']
                temp['basla_num'] = x['basla_num']
                temp['son_num'] = x['son_num']
                rs_a_list.append(temp)
            request.session['rs_a_list'] = rs_a_list
        else:
            rs_okuma = True
            print(" rs okuma....", rs_okuma)
            a_list = []
            for x in a2_list:
                temp = {}
                temp['gelen_tarih'] = parser.parse(x['gelen_tarih'])
                temp['yer'] = x['yer']
                temp['aciklama'] = x['aciklama']
                temp['proje'] = x['proje']
                temp['adi'] = x['adi']
                temp['soyadi'] = x['soyadi']
                temp['progress'] = x['progress']
                temp['basla_num'] = x['basla_num']
                temp['son_num'] = x['son_num']
                a_list.append(temp)

        paginator = Paginator(a_list, 25)
        page = request.GET.get('page')

        try:
            n = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            n = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            n = paginator.page(paginator.num_pages)

        print("işte sayfalanmış liste...", n)
        return render(request, 'islem/ariza_list.html', {'ariza_list': n,})

    else:
        print("buraya geldi...proje yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})




@login_required
def ariza_create(request, pk=None):
    t_stamp = str(datetime.datetime.now())
    tipi = "1"
    proje = "1"
    p_alani = "1"
    yer = "1"
    num = "115"
    rfid_no = "21414016072178"
    rfid_kapat = "12345"
    sebep = "2"
    progress = "1"
    print("okunan zaman......arıza create.............", t_stamp)
    response = requests.post("http://"+settings.ADR_LOCAL+"/ws/ariza_list/",
        json={"mac_no":1234512345, "tipi": tipi, "proje": proje, "p_alani": p_alani, "yer": yer,  "num": num, "rfid_no": rfid_no, "rfid_kapat": rfid_kapat, "sebep": sebep, "progress": progress, "gelen_tarih": t_stamp, "timestamp": t_stamp }, auth=(settings.USER_GLB, settings.PASW_GLB))
    response.json()
    print("status code..", response.status_code)
    return redirect('ariza_list')





@login_required
def mk_ariza_list(request):
    user = request.user
    if sirket_varmi_kontrol(request):
        print("şirket var mı kontrolden geçtik.....")
        sirket = user.profile.sirket
        if request.method == "POST":
            form = SirketIcinProjeForm(request.POST, sirket=sirket)
            if form.is_valid():
                proje = request.POST.get('proje', "")
                print(" proje form okunduktan sonra post...", proje)

                a_list = request.session.get('mk_a_list')
                mk_proje = request.session.get('mk_a_proje')

                if mk_proje == proje:
                    a2_list = []
                    for x in a_list:
                        temp = {}
                        temp['gelen_tarih'] = parser.parse(x['gelen_tarih'])
                        temp['adi'] = x['adi']
                        temp['soyadi'] = x['soyadi']
                        temp['proje'] = x['proje']
                        temp['yer'] = x['yer']
                        temp['aciklama'] = x['aciklama']
                        temp['progress'] = x['progress']
                        temp['basla_num'] = x['basla_num']
                        temp['son_num'] = x['son_num']
                        a2_list.append(temp)

                else:
                    bugun = datetime.datetime.now()
                    yedigun = datetime.timedelta(7,0,0)
                    yedigun_once = bugun - yedigun
                    ariza_obj = Ariza_Data.objects.filter(proje=proje).filter(timestamp__gt=yedigun_once).order_by("-id")
                    a_list = []
                    a2_list = []
                    for x in ariza_obj:
                        temp = {}
                        temp2 = {}
                        temp['gelen_tarih'] = x.gelen_tarih
                        mac_no = x.mac_no
                        yer_obj = yer.objects.filter(mac_no=mac_no).first()
                        if yer_obj:
                            temp['yer'] = yer_obj.yer_adi
                        else:
                            temp['yer'] = mac_no

                        temp['proje'] = x.proje.proje_adi

                        if x.progress == "0":
                            rfid_obj = rfid_dosyasi.objects.filter(rfid_no=x.rfid_no).first()
                        else:
                            rfid_obj = rfid_dosyasi.objects.filter(rfid_no=x.rfid_kapat).first()

                        if rfid_obj:
                            temp['adi'] = rfid_obj.adi
                            temp['soyadi'] = rfid_obj.soyadi
                        else:
                            temp['adi'] = ""
                            temp['soyadi'] = ""

                        sebep = x.sebep
                        print("sebep", sebep)

                        temp['progress'] = x.progress

                        if x.progress == "0":
                            temp['basla_num'] = x.num
                            temp['son_num'] = ""
                        else:
                            temp['basla_num'] = ""
                            temp['son_num'] = x.num

                        if sebep == "1":
                            temp['aciklama'] = "Mekanik"
                        if sebep == "2":
                            temp['aciklama'] = "Elektrik"
                        if sebep == "3":
                            temp['aciklama'] = "Su"
                        if sebep == "4":
                            temp['aciklama'] = "Ayna"

                        temp2['gelen_tarih'] = str(temp['gelen_tarih'])
                        temp2['adi'] = temp['adi']
                        temp2['soyadi'] = temp['soyadi']
                        temp2['proje'] = temp['proje']
                        temp2['yer'] = temp['yer']
                        temp2['aciklama'] = temp['aciklama']
                        temp2['progress'] = temp['progress']
                        temp2['basla_num'] = temp['basla_num']
                        temp2['son_num'] = temp['son_num']
                        a2_list.append(temp)
                        a_list.append(temp2)


                    request.session['mk_a_list'] = a_list
                    request.session['mk_a_proje'] = proje


                paginator = Paginator(a2_list, 25)
                page = request.GET.get('page')
                try:
                    n = paginator.page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    n = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    n = paginator.page(paginator.num_pages)
                print("işte sayfalanmış liste...", n)

                return render(request, 'islem/mk_ariza_list.html', {'form': form, 'mk_ariza_list': n})
            else:
                print("form is invalid.....")
                return redirect('mk_ariza_list')
        else:
            a_list = request.session.get('mk_a_list')
            mk_proje = request.session.get('mk_a_proje')
            a2_list = []
            if a_list:
                for x in a_list:
                    temp = {}
                    temp['gelen_tarih'] = parser.parse(x['gelen_tarih'])
                    temp['adi'] = x['adi']
                    temp['soyadi'] = x['soyadi']
                    temp['deger'] = x['deger']
                    temp['proje'] = x['proje']
                    temp['yer'] = x['yer']
                    temp['aciklama'] = x['aciklama']
                    a2_list.append(temp)
                #print("işte alması gereken m2 list..!!!!!!!!!!!!!!!!!!!!!!!!", m2_list)
            paginator = Paginator(a2_list, 25)
            page = request.GET.get('page')
            try:
                n = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                n = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                n = paginator.page(paginator.num_pages)

            form = SirketIcinProjeForm(sirket=sirket)
            form.fields["proje"].initial = mk_proje
            print("get içinde mi.....")
            #n = ""
            return render(request, 'islem/mk_ariza_list.html', {'form': form, 'mk_ariza_list': n})

    else:
        print("buraya geldi...şirket merkez yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})



#--------------------------------------------------------------------------------------------------

@login_required
def sayi_list(request, pk=None):
    user = request.user
    test_url = str(request.get_full_path)
    print("işte deneme url si.....", test_url)
    src_str = '?page'
    deger = test_url.find(src_str)
    if deger == -1:
        ilk_arama = True
    else:
        ilk_arama = False

    print("değer ....", deger)
    print("ilk_arama", ilk_arama)

    if proje_varmi_kontrol(request):
        print("proje var mı kontrolden geçtik.....")
        proje = user.profile.proje
        sy2_list = request.session.get('rs_sy_list')

        if not (sy2_list) or ilk_arama:
            sy_list = get_sy_list(request)
            rs_sy_list = []
            for x in sy_list:
                temp = {}
                temp['yer'] = x['yer']
                temp['adet'] = x['adet']
                temp['proje'] = x['proje']
                temp['gelen_tarih'] = str(x['gelen_tarih'])
                rs_sy_list.append(temp)
            request.session['rs_sy_list'] = rs_sy_list
        else:
            rs_okuma = True
            print(" rs okuma....", rs_okuma)
            sy_list = []
            for x in sy2_list:
                temp = {}
                temp['gelen_tarih'] = parser.parse(x['gelen_tarih'])
                temp['yer'] = x['yer']
                temp['adet'] = x['adet']
                temp['proje'] = x['proje']
                sy_list.append(temp)

        paginator = Paginator(sy_list, 25)
        page = request.GET.get('page')

        try:
            n = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            n = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            n = paginator.page(paginator.num_pages)

        print("işte sayfalanmış liste...", n)
        return render(request, 'islem/sayi_list.html', {'sayi_list': n,})

    else:
        print("buraya geldi...proje yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})




@login_required
def sayi_create(request, pk=None):
    t_stamp = str(datetime.datetime.now())
    #g_tarih = str(datetime.datetime(2018,7,6,22,0,0))
    g_tarih = str(datetime.datetime.now())
    tipi = "1"
    proje = "1"
    p_alani = "1"
    yer = "1"
    adet = "13"
    print("okunan zaman..sayi create.............", t_stamp)
    response = requests.post("http://"+settings.ADR_LOCAL+"/ws/sayi_list/",
        json={"mac_no":12345, "tipi": tipi, "proje": proje, "p_alani": p_alani, "yer": yer,  "adet": adet, "gelen_tarih": g_tarih, "timestamp": t_stamp }, auth=(settings.USER_GLB, settings.PASW_GLB))
    print("işte response....", response)
    response.json()
    print("status code..", response.status_code)
    return redirect('sayi_list')




@login_required
def mk_sayi_list(request):
    user = request.user
    if sirket_varmi_kontrol(request):
        print("şirket var mı kontrolden geçtik.....")
        sirket = user.profile.sirket
        if request.method == "POST":
            form = SirketIcinProjeForm(request.POST, sirket=sirket)
            if form.is_valid():
                proje = request.POST.get('proje', "")
                print(" proje form okunduktan sonra post...", proje)

                sy_list = request.session.get('mk_sy_list')
                mk_proje = request.session.get('mk_sy_proje')

                if mk_proje == proje:
                    sy2_list = []
                    for x in sy_list:
                        temp = {}
                        temp['gelen_tarih'] = parser.parse(x['gelen_tarih'])
                        temp['adet'] = x['adet']
                        temp['proje'] = x['proje']
                        temp['yer'] = x['yer']
                        sy2_list.append(temp)

                else:
                    bugun = datetime.datetime.now()
                    yedigun = datetime.timedelta(7,0,0)
                    yedigun_once = bugun - yedigun
                    sayi_obj = Sayi_Data.objects.filter(proje=proje).filter(timestamp__gt=yedigun_once).order_by("-id")
                    sy_list = []
                    sy2_list = []
                    for x in sayi_obj:
                        temp = {}
                        temp2 = {}
                        temp['gelen_tarih'] = x.gelen_tarih
                        mac_no = x.mac_no
                        yer_obj = yer.objects.filter(mac_no=mac_no).first()
                        if yer_obj:
                            temp['yer'] = yer_obj.yer_adi
                        else:
                            temp['yer'] = mac_no

                        temp['proje'] = x.proje.proje_adi

                        adet = x.adet
                        print("adet", adet)

                        temp['adet'] = adet

                        temp2['gelen_tarih'] = str(temp['gelen_tarih'])
                        temp2['adet'] = temp['adet']
                        temp2['proje'] = temp['proje']
                        temp2['yer'] = temp['yer']
                        sy2_list.append(temp)
                        sy_list.append(temp2)


                    request.session['mk_sy_list'] = sy_list
                    request.session['mk_sy_proje'] = proje


                paginator = Paginator(sy2_list, 25)
                page = request.GET.get('page')
                try:
                    n = paginator.page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    n = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    n = paginator.page(paginator.num_pages)
                print("işte sayfalanmış liste...", n)

                return render(request, 'islem/mk_sayi_list.html', {'form': form, 'mk_sayi_list': n})
            else:
                print("form is invalid.....")
                return redirect('mk_sayi_list')
        else:
            sy_list = request.session.get('mk_sy_list')
            mk_proje = request.session.get('mk_sy_proje')
            sy2_list = []
            if sy_list:
                for x in sy_list:
                    temp = {}
                    temp['gelen_tarih'] = parser.parse(x['gelen_tarih'])
                    temp['adet'] = x['adet']
                    temp['proje'] = x['proje']
                    temp['yer'] = x['yer']
                    sy2_list.append(temp)
                #print("işte alması gereken m2 list..!!!!!!!!!!!!!!!!!!!!!!!!", m2_list)
            paginator = Paginator(sy2_list, 25)
            page = request.GET.get('page')
            try:
                n = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                n = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                n = paginator.page(paginator.num_pages)

            form = SirketIcinProjeForm(sirket=sirket)
            form.fields["proje"].initial = mk_proje
            print("get içinde mi.....")
            #n = ""
            return render(request, 'islem/mk_sayi_list.html', {'form': form, 'mk_sayi_list': n})

    else:
        print("buraya geldi...şirket merkez yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})



#------------------------------------------------------------------------------------------------------





@login_required
def rapor_memnuniyet(request, pk=None):
    user = request.user
    if proje_varmi_kontrol(request):
        print("şirket var mı kontrolden geçtik.....")
        sirket = user.profile.sirket
        if request.method == "POST":
            form = RaporTarihForm(request.POST)
            if form.is_valid():
                ilk_tarih = request.POST.get('ilk_tarih', "")
                son_tarih = request.POST.get('son_tarih', "")
                #proje = request.POST.get('proje', "")
                print(" proje form okunduktan sonra tarihler...", ilk_tarih, son_tarih)
                return render(request, 'islem/charts.html', {'form': form,  'ilk_tarih': ilk_tarih, 'son_tarih': son_tarih})
            else:
                print("form is invalid.....")
                return redirect('rapor_memnuniyet')
        else:

            form = RaporTarihForm()
            #proje = None
            ilk_tarih = None
            son_tarih = None
            return render(request, 'islem/charts.html', {'form': form,  'ilk_tarih': ilk_tarih, 'son_tarih': son_tarih})

    else:
        print("buraya geldi...şirket merkez yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})


@login_required
def rapor_mk_memnuniyet(request):
    user = request.user
    if sirket_varmi_kontrol(request):
        print("şirket var mı kontrolden geçtik.....")
        sirket = user.profile.sirket
        if request.method == "POST":
            form = Sirket_Mem_RaporForm(request.POST, sirket=sirket)
            if form.is_valid():
                ilk_tarih = request.POST.get('ilk_tarih', "")
                son_tarih = request.POST.get('son_tarih', "")
                proje = request.POST.get('proje', "")
                print(" proje form okunduktan sonra tarihler...", ilk_tarih, son_tarih)
                return render(request, 'islem/charts_mk.html', {'form': form, 'proje': proje, 'ilk_tarih': ilk_tarih, 'son_tarih': son_tarih})
            else:
                print("form is invalid.....")
                return redirect('rapor_mk_memnuniyet')
        else:

            form = Sirket_Mem_RaporForm(sirket=sirket)
            proje = None
            ilk_tarih = None
            son_tarih = None
            return render(request, 'islem/charts_mk.html', {'form': form, 'proje': proje, 'ilk_tarih': ilk_tarih, 'son_tarih': son_tarih})

    else:
        print("buraya geldi...şirket merkez yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})


@login_required
def rapor_krs_memnuniyet(request):
    user = request.user
    if sirket_varmi_kontrol(request):
        print("şirket var mı kontrolden geçtik.....")
        sirket = user.profile.sirket
        if request.method == "POST":
            form = RaporTarihForm(request.POST,)
            if form.is_valid():
                ilk_tarih = request.POST.get('ilk_tarih', "")
                son_tarih = request.POST.get('son_tarih', "")
                #proje = request.POST.get('proje', "")
                print(" proje form okunduktan sonra tarihler...", ilk_tarih, son_tarih)
                return render(request, 'islem/charts_krs.html', {'form': form, 'ilk_tarih': ilk_tarih, 'son_tarih': son_tarih})
            else:
                print("form is invalid.....")
                return redirect('rapor_krs_memnuniyet')
        else:

            form = RaporTarihForm()
            #proje = None
            ilk_tarih = None
            son_tarih = None
            return render(request, 'islem/charts_krs.html', {'form': form,  'ilk_tarih': ilk_tarih, 'son_tarih': son_tarih})

    else:
        print("buraya geldi...şirket merkez yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})



#---------------------yer bazında günlük analiz-------------------------------------

@login_required
def gunluk_yer(request, pk=None):
    user = request.user
    if proje_varmi_kontrol(request):
        print("şirket var mı kontrolden geçtik.....")
        sirket = user.profile.sirket
        proje = user.profile.proje
        if request.method == "POST":
            form = YerSecForm(request.POST, proje=proje)
            if form.is_valid():
                yersec = request.POST.get('yersec', "")
                tarih = datetime.datetime.now()
                #tarih = datetime.datetime(12,12,12)


                context = { 'form': form,
                }
                return render(request, 'islem/gunluk_yer.html', context )
            else:
                print("form is invalid.....")
                return redirect('gunluk_yer')
        else:

            form = YerSecForm(proje=proje)
            context = { 'form': form,
                }
            return render(request, 'islem/gunluk_yer.html', context)

    else:
        print("buraya geldi...şirket merkez yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})







#--------------------------------------------------------------------------------------------------
# rfid dosyası, web service işlemleri
@login_required
def rfid_list(request, pk=None):
    rfid_list = get_rfid_list()
    print("rfid list..", rfid_list)
    return render(request, 'islem/rfid_list.html', {'rfid_list': rfid_list,})




@login_required
def rfid_filter(request):

    if request.method == "POST":
        form = RfidProjeForm(request.POST)
        if form.is_valid():
            proje = request.POST.get('proje', "")
            print(" proje form okunduktan sonra post...", proje)
            url = "http://"+settings.ADR_LOCAL+"/ws/rfid_filter/"+str(proje)+"/"
            print("işte url", url)
            response = requests.get(url, auth=(settings.USER_GLB, settings.PASW_GLB))
            print("response...", response)
            gelen = response.json()
            print("gelen deger mac bul içinden...", gelen)
            return render(request, 'islem/rfid_proje.html', {'form': form, 'gelen': gelen})
    else:
        form = RfidProjeForm()
        gelen = ""
    return render(request, 'islem/macnoyer.html', {'form': form, 'gelen': gelen})



@login_required
def rfid_filter_proje(request, proje=None):
    print("rfid project list............", proje)
    r = requests.get_queryset("http://"+settings.ADR_LOCAL+"/ws/rfid_filter" + str(proje) + "/",  auth=(settings.USER_GLB, settings.PASW_GLB))
    json_data = r.json()
    print(json_data)

    rfid_list = json_data
    print("rfid list..", rfid_list)
    return render(request, 'islem/rfid_list.html', {'rfid_list': rfid_list,})

@login_required
def rfid_create(request, pk=None):
    t_stamp = str(datetime.datetime.now())
    tipi = "1"
    rfid_no = "3"
    sebep = "6"
    print("okunan zaman......menuniyet create.............", t_stamp)
    response = requests.post("http://"+settings.ADR_LOCAL+"/ws/rfid_list/",
        json={"mac_no":123451234512345, "tipi": tipi, "rfid_no": rfid_no, "sebep": sebep, "gelen_tarih": t_stamp, "timestamp": t_stamp }, auth=(settings.USER_GLB, settings.PASW_GLB))
    response.json()
    print("status code..", response.status_code)
    return redirect('ariza_list')







#--------------------------------------------------------------------------------------------------
from operator import attrgetter, itemgetter

@login_required
def yerud_list(request, pk=None):
    user = request.user
    if proje_varmi_kontrol(request):
        print("proje var mı kontrolden geçtik.....")
        proje = user.profile.proje
        yerud_obj = yer_updown.objects.filter(proje=proje).order_by("id")
        y_list = []
        for x in yerud_obj:
            temp = {}

            temp['id'] = x.id
            temp['mac_no'] = x.mac_no
            yer_obj = yer.objects.filter(mac_no=x.mac_no).first()
            if yer_obj:
                temp['yer'] = yer_obj.yer_adi
            else:
                temp['yer'] = ""

            temp['proje'] = x.proje.proje_adi
            temp['degis'] = x.degis
            temp['alive_time'] = x.alive_time

            y_list.append(temp)

        print("y list.....", y_list)

        sorted_y = sorted(y_list, key=itemgetter('yer'))

        print("sorted y....", sorted_y)

        #paginator = Paginator(y_list, 20)
        paginator = Paginator(sorted_y, 20)
        page = request.GET.get('page')
        try:
            n = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            n = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            n = paginator.page(paginator.num_pages)
        print("işte sayfalanmış liste...", n)

        return render(request, 'islem/yerud_list.html', {'yerud_list': n,})

    else:
        print("buraya geldi...proje yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})



@login_required
def ad_yerud_list(request):
    user = request.user
    if admin_kontrol(request):
        print("admin kontrolden geçtik.....")
        if request.method == "POST":
            form = Sirket_Proje_Form(request.POST)
            if form.is_valid():
                proje = request.POST.get('proje', "")
                print(" proje form okunduktan sonra post...", proje)

                yerud_obj = yer_updown.objects.filter(proje=proje).order_by("id")
                y_list = []
                for x in yerud_obj:
                    temp = {}

                    temp['id'] = x.id
                    temp['mac_no'] = x.mac_no
                    yer_obj = yer.objects.filter(mac_no=x.mac_no).first()
                    if yer_obj:
                        temp['yer'] = yer_obj.yer_adi
                    else:
                        temp['yer'] = ""

                    temp['proje'] = x.proje.proje_adi
                    temp['degis'] = x.degis
                    temp['alive_time'] = x.alive_time

                    y_list.append(temp)

                print("y list.....", y_list)

                sorted_y = sorted(y_list, key=itemgetter('yer'))

                print("sorted y....", sorted_y)


                return render(request, 'islem/ad_yerud_list.html', {'form': form, 'ad_yerud_list': sorted_y})
            else:
                print("form is invalid.....")
                return redirect('ad_yerud_list')
        else:


            form = Sirket_Proje_Form()
            n = ""
            return render(request, 'islem/ad_yerud_list.html', {'form': form, 'ad_yerud_list': n})

    else:
        print("buraya geldi...şirket merkez yetkilisi değil...")
        mesaj = "kişi bu işlem için yetkili değil..."
        return render(request, 'islem/uyari.html', {'mesaj': mesaj})







@login_required
def yerud_create(request, pk=None):
    t_stamp = str(datetime.datetime.now())
    tipi = "1"
    rfid_no = "3"
    sebep = "6"
    print("okunan zaman......yerud create.............", t_stamp)
    response = requests.post("http://"+settings.ADR_LOCAL+"/ws/yerud_list/",
        json={"mac_no":123451234512345, "tipi": tipi, "rfid_no": rfid_no, "sebep": sebep, "gelen_tarih": t_stamp, "timestamp": t_stamp }, auth=(settings.USER_GLB, settings.PASW_GLB))
    response.json()
    print("status code..", response.status_code)
    return redirect('yerud_list')



@login_required
def yerud_detail_get(request, pk=None):
    mac_no = pk
    print("gelen mac degeri...", mac_no)
    url = "http://"+settings.ADR_LOCAL+"/ws/yerud_detail/"+str(mac_no)+"/"
    print("işte url", url)
    response = requests.get(url, auth=(settings.USER_GLB, settings.PASW_GLB))
    print("response...", response)
    gelen = response.json()
    print("gelen deger mac bul içinden...", gelen)
    return redirect('yerud_list')



#---------------------------------------------------------------------------------------

@login_required
def sms_mesaj(request, pk=None):
    sms_result = get_sms()
    print("sms result..", sms_result)
    sayı = len(sms_result)
    print("dönen mesaj listesinin uzunluğu...", sayı)
    kod = sms_result[0]
    if sayı == 2:
        ek_kod = sms_result[1]
    else:
        ek_kod = ""
    print("kod", kod)
    print("ek kod", ek_kod)
    return render(request, 'islem/sms_result.html', {'sms_result': sms_result,})


#---------------------------------------------------------------------------------------

from django.template import RequestContext

# HTTP Error 400
def my_400_bad_request_view(request):
    data = {}
    return render(request,'islem/hata_400.html', data)

# HTTP Error 403
def my_403_permission_denied_view(request):
    data = {}
    return render(request,'islem/hata_403.html', data)

# HTTP Error 404
def my_404_page_not_found_view(request):
    data = {}
    return render(request,'islem/hata_400.html', data)

# HTTP Error 500
def my_500_error_view(request):
    data = {}
    return render(request,'islem/hata_500.html', data)





@login_required
def macnoyer(request):
    kullanici = request.user.id
    kullanici_obj = Profile.objects.get(user=kullanici)
    proje = kullanici_obj.proje
    print("kullanıcı ve projesi", kullanici, "-",  proje)

    if request.method == "POST":
        form = MacnoYerForm(request.POST)
        if form.is_valid():
            macnoyer = request.POST.get('macnoyer', "")
            print(" macnoyer form okunduktan sonra post...", macnoyer)
            yerud_obj = yer_updown.objects.get(id=macnoyer)
            gelen_macno = yerud_obj.mac_no

            url = "http://"+settings.ADR_LOCAL+"/ws/yerud_detail/"+str(gelen_macno)+"/"
            print("işte url", url)
            response = requests.get(url, auth=(settings.USER_GLB, settings.PASW_GLB))
            print("response...", response)
            gelen = response.json()
            print("gelen deger mac bul içinden...", gelen)
            return render(request, 'islem/macnoyer.html', {'form': form, 'gelen': gelen})
    else:
        form = MacnoYerForm()
        gelen = ""
    return render(request, 'islem/macnoyer.html', {'form': form, 'gelen': gelen})


@login_required
def macnoyer_degis(request):
    kullanici = request.user.id
    kullanici_obj = Profile.objects.get(user=kullanici)
    proje = kullanici_obj.proje
    print("kullanıcı ve projesi", kullanici, "-",  proje)

    if request.method == "POST":
        form = MacnoYerForm(request.POST)
        if form.is_valid():
            macnoyer = request.POST.get('macnoyer', "")
            print(" macnoyer form okunduktan sonra post...", macnoyer)
            yerud_obj = yer_updown.objects.get(id=macnoyer)
            gelen_macno = yerud_obj.mac_no

            url = "http://"+settings.ADR_LOCAL+"/ws/yerud_detail/"+str(gelen_macno)+"/"
            print("işte url", url)
            response = requests.get(url, auth=(settings.USER_GLB, settings.PASW_GLB))
            print("response...", response)
            gelen = response.json()

            gl_url = gelen['url']
            gl_id = gelen['id']
            gl_mac_no = gelen['mac_no']
            gl_proje = gelen['proje']
            gl_degis = gelen['degis']
            gl_alive_time = gelen['alive_time']

            print("gelen url..", gl_url)
            print("gelen id..", gl_id)
            print("gelen mac_no..", gl_mac_no)
            print("gelen proje..", gl_proje)
            print("gelen degis..", gl_degis)
            print("gelen alive_time..", gl_alive_time)



            data = {
                    "url": gl_url,
                    "id": gl_id,
                    "mac_no": gl_mac_no,
                    "proje": gl_proje,
                    "degis": "H",
                    "alive_time": gl_alive_time
                    }
            response = requests.put(url, data=data , auth=(settings.USER_GLB, settings.PASW_GLB))

            response = requests.get(url, auth=(settings.USER_GLB, settings.PASW_GLB))
            print("response...", response)
            gelen = response.json()
            print("gelen deger mac bul içinden...", gelen)
            return render(request, 'islem/macnoyer.html', {'form': form, 'gelen': gelen})
    else:
        form = MacnoYerForm()
        gelen = ""
    return render(request, 'islem/macnoyer.html', {'form': form, 'gelen': gelen})



#--------------------------------------------------------------
@login_required
class RfidListView(LoginRequiredMixin,generic.ListView):
    model = rfid_dosyasi
    paginate_by = 20


@login_required
class RfidDetailView(LoginRequiredMixin,generic.DetailView):
    model = rfid_dosyasi


#------------------------------------------------------------------------------------
@login_required
def show_notification(request, notification_id):
    n = Notification.objects.get(id=notification_id)
    return render_to_response('islem/bildirimler.html', {'notification': n})

@login_required
def delete_notification(request, notification_id, page_id):
    #print("delete notification içinden n id............", notification_id, "page id.....", page_id)
    #print("///////////////////////////////////////////////////////////////")
    n = Notification.objects.get(id=notification_id)
    n.viewed = True
    n.save()
    #return redirect('list_notification')
    url_notif = '/islem/notification/?page='+str(page_id)
    return redirect(url_notif)


@login_required
def create_notification(request):
    print("create notification kısmı...")
    print("request.user.id", request.user.id)
    Notification.objects.create(kisi_id=request.user.id,
                                proje_id=2,
                                title="title deneme......",
                                message="mesaj deneme..........")
    return redirect('index')

@login_required
def list_notification(request):
    print("list notifications ..")
    print("request user id..", request.user.id)
    #n = Notification.objects.all()
    proje = request.user.profile.proje
    bugun = datetime.datetime.now()
    yedigun = datetime.timedelta(14,0,0)
    yedigun_once = bugun - yedigun
    print("yedi gün önce ...............", yedigun_once)
    #liste proje bazından kişi bazına çevrildi...1 ekim 2018...
    n_list = Notification.objects.filter(viewed=False).filter(timestamp__gt=yedigun_once).filter(kisi=request.user.id).order_by("-id")
    #contact_list = Contacts.objects.all()
    paginator = Paginator(n_list, 25)
    page = request.GET.get('page')
    print("işte page.....", page)
    print(".........................................")
    try:
        n = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        n = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        n = paginator.page(paginator.num_pages)
    print("işte sayfalanmış liste...", n)
    return render_to_response('islem/bildirimler.html', {'notification_list': n,
                                                         'user':request.user,
                                                          })

#-------------------------------------------------------------------------------------
@login_required
def deneme_dropdown(request):
    return render(request, 'notif_test.html')

#-------------------------------------------------------------------------------
@login_required
def xyz(request):
    denetim_obj = denetim.objects.all().order_by('denetim_adi')
    #content = unicode(content)
    #denetim_obj = str(denetim_obj)
    return render(request, 'islem/xyz.html', {'denetim_obj': denetim_obj} )


#-------------------------------------------------------------------------------
@login_required
def kamera(request):
    denetim_obj = denetim.objects.all().order_by('denetim_adi')
    #content = unicode(content)
    #denetim_obj = str(denetim_obj)
    return render(request, 'islem/kamera.html', {'denetim_obj': denetim_obj} )
