from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.template.loader import get_template
from islem.utils import render_to_pdf #created in step 4
import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import grup, sirket, proje, tipi, bolum, detay, acil, isaretler, zon
from .models import Profile, denetim, sonuc_detay, sonuc_bolum, kucukresim, sonuc_takipci
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models, transaction
from islem.forms import BolumSecForm, SonucForm, DenetimSecForm
from islem.forms import DenetimForm,  IkiliSecForm, ProjeSecForm
from islem.forms import IlkDenetimSecForm, KucukResimForm
from islem.forms import AcilAcForm, AcilKapaForm, AcilDenetimSecForm
from islem.forms import Denetim_Deneme_Form, Ikili_Deneme_Form, NebuForm, Den_Olustur_Form
import collections
from django.contrib.admin.widgets import FilteredSelectMultiple

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

import json
import requests

#from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist




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
        response['Content-Disposition'] = 'attachment; filename="report_example.pdf"'
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

    if kullanici.denetci == "E":
        acik_denetimler = denetim.objects.filter(durum="A")
        acik_denetimler_sirali = acik_denetimler.order_by('hedef_baslangic')
        secili_denetimler = acik_denetimler_sirali.filter(denetci=request.user)
        return render(request, 'ana_menu.html',
            context={
            'secili_denetimler': secili_denetimler,
            },
        )
    else:
        num_tipi=tipi.objects.all().count()
        num_bolum=bolum.objects.all().count()
        num_detay=detay.objects.all().count()

        num_grup=grup.objects.all().count()
        num_sirket=sirket.objects.all().count()
        num_proje=proje.objects.count()

        return render(request, 'ana_menu_eski.html',
            context={
                'num_tipi':num_tipi,
                'num_bolum':num_bolum,
                'num_detay':num_detay,

                'num_grup': num_grup,
                'num_sirket': num_sirket,
                'num_proje': num_proje,
                },
            )



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
               'durum' : durum,
               'islem_olsun' : islem_olsun,
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

# denetimi başlatmaya karar verildiğinde durumu C yapıyor, B den C ye

@login_required
def denetim_baslat_kesin(request, pk=None):

    denetim_no = request.session.get('denetim_no')
    request.session['devam_tekrar'] = "devam"
    denetim_obj = denetim.objects.get(id=denetim_no)
    print("seçilen denetim kesin ...", denetim_obj)
    denetim_obj.durum = "B"
    denetim_obj.save()
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
    devameden_denetimler_sirali = devameden_denetimler.order_by('hedef_baslangic')
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
            dd_denetim_2 = int(dd_denetim)
            print ("denetim ", dd_denetim_2)
            dd_konu = request.POST.get('konu', "")
            print ("konu", dd_konu)
            dd_aciklama = request.POST.get('aciklama', "")
            print ("aciklama", dd_aciklama)
            # veri tabanına yazıyor
            acil_obj, created = acil.objects.get_or_create(denetim_id=dd_denetim_2)

            if created:
                # means you have created a new db objects
                print("id  bir", acil_obj.id)
                print("denetim", acil_obj.denetim)
                kaydetme_obj = acil(denetim_id=acil_obj.denetim, konu=dd_konu, aciklama=dd_aciklama)
                kaydetme_obj.save()
            else:
                # just refers to the existing one
                print("id  iki", acil_obj.id)
                print("denetim", acil_obj.denetim)
                kaydetme_obj = acil(id=acil_obj.id, denetim_id=acil_obj.denetim, konu=dd_konu, aciklama=dd_aciklama)
                kaydetme_obj.save()


            denetim_no = acil_obj.denetim.id
            print("denetim no...", denetim_no)
            denetim_obj = denetim.objects.get(id=denetim_no)
            denetci = denetim_obj.denetci
            takipci_obj = sonuc_takipci.objects.filter(denetim=denetim_no)

            #############---------------------------------------------
            #email işlemi---------------------------------------------
            #############----------------------------------------------

            connection = mail.get_connection()
            connection.open()

            adi = denetim_obj.denetci.get_full_name()
            denetim_id = denetim_obj.id
            denetim_adi = denetim_obj.denetim_adi
            baslangic = denetim_obj.hedef_baslangic
            bitis = denetim_obj.hedef_bitis

            subject = "Denetçi tarafından acil bildirim"
            to = [denetim_obj.denetci.email]
            from_email = settings.EMAIL_HOST_USER
            ctx = {
                'adi': adi,
                'denetim_adi': denetim_adi,
                'konu': dd_konu,
                'aciklama': dd_aciklama
                }
            message = get_template('islem/emt_acil_bildirim.html').render(ctx)
            msg = EmailMessage(subject, message, to=to, from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()

            takipci_obj = sonuc_takipci.objects.filter(denetim=denetim_id)

            for takipci in takipci_obj:
                adi = takipci.takipci.get_full_name()
                subject = "Denetçi tarafından acil bildirim"
                to = [takipci.takipci.email]
                from_email = settings.EMAIL_HOST_USER
                ctx = {
                    'adi': adi,
                    'denetim_adi': denetim_adi,
                    'konu': dd_konu,
                    'aciklama': dd_aciklama
                    }
                message = get_template('islem/emt_acil_bildirim.html').render(ctx)
                msg = EmailMessage(subject, message, to=to, from_email=from_email)
                msg.content_subtype = 'html'
                msg.send()

            connection.close()

            # email işlemi sonu.....................

            messages.success(request, 'Acil bildirimi gönderildi.......')
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

    return redirect('denetim_bolum_sec' )


#--------------------------------------------------------------------
#  denetimi tamamlama işlemleri önce sor sonra tamamla


@login_required
def denetim_tamamla(request, pk=None):

    denetim_no = request.session.get('denetim_no')
    denetim_obj = denetim.objects.get(id=pk)
    print("seçilen denetim", denetim_obj)

    ilk_obje = sonuc_bolum.objects.filter(denetim=denetim_no)
    kontrol_degiskeni = True
    for obje in ilk_obje:
        if obje.tamam == "H":
            kontrol_degiskeni = False

    if kontrol_degiskeni:
        numarasi = denetim_obj.id
        denetim_adi = denetim_obj.denetim_adi
        context = {'denetim_adi': denetim_adi,
                   'numarasi' : numarasi,
                }
        return render(request, 'islem/denetim_tamamla_sor.html', context )

    else:
        messages.success(request, 'Tamamlanmamış bölümler var.......')
        return redirect('devam_liste')


#--------------------------------------------------------------------------------

# denetim artık tamamlanıyor C - D yapılıyor....

@login_required
def denetim_tamamla_kesin(request, pk=None):

    denetim_no = request.session.get('denetim_no')
    denetim_obj = denetim.objects.get(id=pk)
    print("seçilen denetim kesin ...", denetim_obj)
    denetim_obj.durum = "C"
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
                messages.success(request, 'Seçili bölümde bölüm detayı yok....')
                return redirect('denetim_baslat')
            #form = DetayForm(denetim_no=denetim_no, secili_bolum=secili_bolum)
            form = SonucForm(puanlama_turu="")
            print("puanlama türü boş olarak ilk adımda çalıştı ama nasıl ????????????")
            return render(request, 'islem/denetim_detay_islemleri.html')


        else:
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
                messages.success(request, 'Bölüm işlemleri tamamlanmış....')
                return redirect('index')

        form = BolumSecForm(denetim_no=denetim_no, devam_tekrar=devam_tekrar)
        return render(request, 'islem/denetim_bolum_sec.html', {'form': form,})



#--------------------------------------------------------------------------
# js içinden işlem yapılacak bölümü seçiyor....
# seçilen bölümü oturum değişkenine yazıyor

def secilen_bolumu_kaydet(request):
    print("seçilen bölümü kaydet ......")
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
        form = DenetimForm(request.POST or None, bolum_listesi=bolum_listesi, init_param=init_param )
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
                    print("bölüm no", bolum_no, "olmalı bölüm :", olmali_bolum)
                    if bolum_no == olmali_bolum:
                        kaydet_obj = sonuc_detay(denetim_id=denetim_no,
                                                    bolum_id=bolum_no,
                                                    detay_id=detay_no
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

            messages.success(request, 'denetim başarıyla kaydedildi......')
            #return render(request, 'islem/tek_sayfa.html', context,)
            return redirect('index')
        else:
            print("ne oldu be kardeşim...........")
            messages.success(request, ' form hatası - tekrar deneyin....')
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
        form = DenetimForm(bolum_listesi=bolum_listesi, init_param=init_param)
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
            js_denetci = denetim_obj.denetci.id
            js_tipi = denetim_obj.tipi.id
            js_hedef_baslangic = denetim_obj.hedef_baslangic
            js_hedef_bitis = denetim_obj.hedef_bitis
            js_aciklama = denetim_obj.aciklama

            print("denetim no", js_denetim_no)
            print("denetim adi", js_denetim_adi)
            print("proje", js_proje)
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
        form = DenetimForm(request.POST or None, bolum_listesi=bolum_listesi, init_param=init_param)

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
                    olmali_bolum = detayli_obj.bolum
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
            messages.success(request, 'denetim başarıyla kaydedildi......')
            #return render(request, 'islem/tek_sayfa.html', context,)
            return redirect('index')
        else:
            print("ne oldu be kardeşim...........")
            messages.success(request, ' form hatası - tekrar deneyin....')
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

        form = DenetimForm(bolum_listesi=bolum_listesi, init_param=init_param)
        form.fields["pk_no"].initial = js_denetim_no
        form.fields["denetim_adi"].initial = js_denetim_adi
        form.fields["proje"].initial = js_proje
        form.fields["rp_hidden"].initial = js_rutin_planli
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

        request.session['bolum_listesi'] = bolum_listesi
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

    messages.success(request, 'Başarıyla silindi....')
    return redirect('index')











#--------------------------------------------------------------------------------

# js içinden tamam butonu ile çalışıyor...
# bölüm seçildiğinde bu bölümde detay var mı diye bakıp
# sonrasında bu bölümdeki tüm detaylar H yapıp detayları sifirlıyor...

@login_required
def detay_islemleri_baslat(request, pk=None):
    print("denetim işlemleri başlat......")
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
            messages.success(request, 'Seçili bölümde bölüm detayı yok....')
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


@csrf_protect
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

        bir = sonuc_detay.objects.filter(denetim=denetim_no)
        iki = bir.filter(bolum=secili_bolum)
        bulunan = iki.get(detay=secili_detay)
        #bulunan = get_object_or_404(sonuc, detay=secili_detay)
        detay_obj = detay.objects.get(id=secili_detay)
        puanlama_turu = detay_obj.puanlama_turu
        print(" puanlama türü...", puanlama_turu)

        form = SonucForm(request.POST or None, request.FILES or None, instance=bulunan, puanlama_turu=puanlama_turu)

        if form.is_valid():
            print("neyse ki valid..bin...ext...")
            # bu detay için tamamı E yap, yani tamamlandı....sonra update yap...
            edit = form.save(commit=False)
            edit.tamam = "E"
            edit.puanlama_turu = puanlama_turu
            resim_obj = kucukresim.objects.get(kullanici=request.user.id)
            kucuk_resim = resim_obj.foto_kucuk
            edit.foto = kucuk_resim
            edit.save()
            print("kaydetmiş olması lazım.................")

            # bir sonraki................
            # için  işlem yap................
            ilk_detaylar = sonuc_detay.objects.filter(denetim=denetim_no)
            print("ilk detaylar..denetim detay işlemleri :", ilk_detaylar)
            detaylar = ilk_detaylar.filter(bolum=secili_bolum)
            print("detaylar.. denetim detay işişlemleri..:", detaylar)
            secili_detay_obj = detaylar.filter(tamam="H")
            print("seçili detaylar tamam H olanlar...", secili_detay_obj)

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
                    messages.success(request, 'Bölüm içindeki denetim detay işlemleri tamamlandı....')
                    return redirect('denetim_bolum_sec')
                else:
                    messages.success(request, 'Bölüm içindeki denetim detay işlemleri tamamlandı....')
                    return redirect('devam_liste')

            secili_obj = secili_detay_obj.first()
            secili_detay = secili_obj.detay.id
            print("secili - detay.... bakalım  doğru mu...", secili_detay)
            request.session['secili_detay'] = secili_detay

            detay_obj = detay.objects.get(id=secili_detay)
            puanlama_turu = detay_obj.puanlama_turu
            print(" puanlama türü...", puanlama_turu)

            form = SonucForm(puanlama_turu=puanlama_turu)
            context = { 'form': form,
                        'secili_obj' : secili_obj,
                        }
            return render(request, 'islem/denetim_detay_islemleri.html', context,)


        else:
            print("ne oldu be kardeşim...........")
            messages.success(request, ' form hatası - tekrar deneyin....')
            return redirect('devam_liste')
            #return render(request, 'islem/denetim_bolum_sec.html', {'form': form,})

    # if a GET (or any other method) we'll create a blank form
    else:
        ilk_detaylar = sonuc_detay.objects.filter(denetim=denetim_no)
        print("ilk detaylar..denetim detay işlemleri :", ilk_detaylar)
        detaylar = ilk_detaylar.filter(bolum=secili_bolum)
        print("detaylar.. denetim detay işişlemleri..:", detaylar)
        secili_detay_obj = detaylar.filter(tamam="H")
        print("seçili detaylar tamam H olanlar...", secili_detay_obj)

        if not secili_detay_obj:
            messages.success(request, 'Bölüm içinde detay işlemleri tamamlandı....')
            return redirect('denetim_bolum_sec')
        secili_obj = secili_detay_obj.first()
        secili_detay = secili_obj.detay.id

        detay_obj = detay.objects.get(id=secili_detay)
        puanlama_turu = detay_obj.puanlama_turu
        print(" puanlama türü...", puanlama_turu)

        print("secili - detay.... bakalım  doğru mu...", secili_detay)
        request.session['secili_detay'] = secili_detay
        form = SonucForm(puanlama_turu=puanlama_turu)
        context = { 'form': form,
                    'secili_obj' : secili_obj,
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
        form = DenetimSecForm(request.POST, denetci=denetci)
        # check whether it's valid:
        if form.is_valid():
            denetim_no = request.POST.get('denetim_no', "")
            print ("denetim seçim yapılmış...", denetim_no)
            request.session['secilen_denetim'] = denetim_no
            sonuc_list = sonuc_detay.objects.filter(denetim=denetim_no).order_by('bolum')
            denetimin_adi = sonuc_list.first().denetim
            denetimin_durumu = sonuc_list.first().denetim.durum
            context = {'sonuc_list': sonuc_list, 'denetimin_adi': denetimin_adi, 'denetimin_durumu': denetimin_durumu}
            return render(request, 'islem/sonuc_list.html', context)
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
        form = DenetimSecForm(denetci=denetci)
        return render(request, 'islem/sonuc_denetim_form.html', {'form': form,})



from django.views.decorators.csrf import csrf_exempt


@login_required
@csrf_exempt
def kucuk_resim_al(request):
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
        else:
            print("bu ibnenin nesi valid değil anlamadım ki......")
    print ("son nokta  küçük resim al....", response_data)
    return HttpResponse(response_data, content_type='application/json')


#--------------------------------------------------------------------------------


@login_required
def qrcode_tara(request, pk=None):

        context = {}
        return render(request, 'islem/qrcode_islemleri.html', context )




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
        messages.success(request, 'Takipçi girilmemiş....')
        return redirect('isemri_denetim_sec')
    if not(bol_varmi):
        messages.success(request, 'Bölümler girilmemiş....')
        return redirect('isemri_denetim_sec')
    if not(det_varmi):
        messages.success(request, 'Detaylar girilmemiş....')
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
        messages.success(request, 'Takipçi girilmemiş....')
        return redirect('isemri_denetim_sec')
    if not(bol_varmi):
        messages.success(request, 'Bölümler girilmemiş....')
        return redirect('isemri_denetim_sec')
    if not(det_varmi):
        messages.success(request, 'Detaylar girilmemiş....')
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
    messages.success(request, 'Denetim iptal edildi....')
    return redirect('index' )


#--------------------------------------------------------------------------------


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
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('tipi')
    messages.success(request, 'Başarıyla silindi....')
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
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('zon')
    messages.success(request, 'Başarıyla silindi....')
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
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('bolum')
    messages.success(request, 'Başarıyla silindi....')
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
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('detay')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('detay')




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
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('grup')
    messages.success(request, 'Başarıyla silindi....')
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
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('sirket')
    messages.success(request, 'Başarıyla silindi....')
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
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('proje')
    messages.success(request, 'Başarıyla silindi....')
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
    #paginate_by = 20

class TipiDetailView(LoginRequiredMixin,generic.DetailView):
    model = tipi

#--------------------------------------------------------------

class ZonListView(LoginRequiredMixin,generic.ListView):
    model = zon
    #paginate_by = 20

class ZonDetailView(LoginRequiredMixin,generic.DetailView):
    model = zon

#--------------------------------------------------------------


class BolumListView(LoginRequiredMixin,generic.ListView):
    model = bolum
    #paginate_by = 20

class BolumDetailView(LoginRequiredMixin,generic.DetailView):
    model = bolum

#-----------------------------------------------------------

class DetayListView(LoginRequiredMixin,generic.ListView):
    model = detay

class DetayDetailView(LoginRequiredMixin,generic.DetailView):
    model = detay

#--------------------------------------------------------------

class GrupListView(LoginRequiredMixin,generic.ListView):
    model = grup
    #paginate_by = 20

class GrupDetailView(LoginRequiredMixin,generic.DetailView):
    model = grup

#---------------------------------------------------------

class SirketListView(LoginRequiredMixin,generic.ListView):
    model = sirket
    #paginate_by = 20

class SirketDetailView(LoginRequiredMixin,generic.DetailView):
    model = sirket

#------------------------------------------------------------

class ProjeListView(LoginRequiredMixin,generic.ListView):
    model = proje

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



@login_required
def deneme_denetim(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Denetim_Deneme_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            messages.success(request, 'Başarıyla oldu bu iş....')
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
        print("qs....", qs)
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
            messages.success(request, 'Başarıyla oldu bu iş....')
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
            messages.success(request, 'Başarıyla oldu bu iş....')
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

#-----------------------------------------------------------------------------------------

class takipciautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
            #return sonuc_bolum.objects.none()

        #qs = Profile.objects.filter(denetim_takipcisi="E")
        qs = User.objects.all()
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
            zon_obj = zon.objects.filter(tipi=bolum_tipi)
            for zonlar in zon_obj:
                print("zonlar id..", zonlar.id)
                qx = bolum.objects.filter(zon=zonlar.id)
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
        qs = detay.objects.all()
        if self.q:
            qs = qs.filter(detay_adi__icontains=self.q)
        return qs


class tipiautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return tipi.objects.none()
        qs = tipi.objects.all()
        if self.q:
            qs = qs.filter(tipi_adi__icontains=self.q)
        return qs

class zonautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return zon.objects.none()
        qs = zon.objects.all()
        if self.q:
            qs = qs.filter(zon_adi__icontains=self.q)
        return qs



class projeautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return proje.objects.none()
        qs = proje.objects.all()
        if self.q:
            qs = qs.filter(proje_adi__icontains=self.q)
        return qs

class denetciautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return user.objects.none()
        qs = Profile.objects.filter(denetci="E")
        if self.q:
            qs = qs.filter(user__username__icontains=self.q)
        return qs




#-------------------------------------------------------------------------------

def xyz(request):
    denetim_obj = denetim.objects.all().order_by('denetim_adi')
    #content = unicode(content)
    #denetim_obj = str(denetim_obj)
    return render(request, 'islem/xyz.html', {'denetim_obj': denetim_obj} )


#-------------------------------------------------------------------------------

def kamera(request):
    denetim_obj = denetim.objects.all().order_by('denetim_adi')
    #content = unicode(content)
    #denetim_obj = str(denetim_obj)
    return render(request, 'islem/kamera.html', {'denetim_obj': denetim_obj} )
