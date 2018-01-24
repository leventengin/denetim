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
from .models import grup, sirket, musteri, tipi, bolum, detay, acil
from .models import Profile, denetim, gozlemci, sonuc, sonuc_bolum, kucukresim
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models, transaction
from islem.forms import GozlemciForm, BolumSecForm, DetayForm, SonucForm, DenetimSecForm
from islem.forms import Denetim_BForm, DenetimForm, IlkBolumForm, IlkDetayForm, IkiliSecForm
from islem.forms import IlkDenetimSecForm, KucukResimForm, YeniDenetciSecForm, YeniTarihForm
from islem.forms import MyForm, MusteriSecForm, AcilAcForm, AcilKapaForm, AcilDenetimSecForm
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
from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)





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
        musteri = denetim_obj.musteri
        denetci = denetim_obj.denetci
        tipi = denetim_obj.tipi
        yaratim_tarihi = denetim_obj.yaratim_tarihi
        yaratan = denetim_obj.yaratan
        hedef_baslangic = denetim_obj.hedef_baslangic
        hedef_bitis = denetim_obj.hedef_bitis
        gerc_baslangic = denetim_obj.gerc_baslangic
        gerc_bitis = denetim_obj.gerc_bitis
        gozlemci_obj = gozlemci.objects.filter(denetim=denetim_no)
        i = 0
        g = []
        for gozlem in gozlemci_obj:
            g.append(gozlem.gozlemci)
            i = i + 1
        d = collections.defaultdict(list)
        bolum_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
        for bolum in bolum_obj:
            print("bolum list . bolum", bolum.bolum)
            detay_obj = sonuc.objects.filter(denetim=denetim_no, bolum=bolum.bolum)
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
                    'g': g,
                    'denetim_adi': denetim_adi,
                    'musteri' : musteri,
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


from .forms import DetayForm


def upload_file(request):
    if request.method == 'POST':
        form = SonucForm(request.POST, request.FILES)
        if form.is_valid():
            instance = sonuc(foto=request.FILES['file'])
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
        acik_denetimler = denetim.objects.filter(durum="B")
        acik_denetimler_sirali = acik_denetimler.order_by('hedef_baslangic')
        secili_denetimler = acik_denetimler_sirali.filter(denetci=request.user)
        return render(request, 'ana_menu.html',
            context={
            'secili_denetimler': secili_denetimler,
            },
        )
    else:
        #return render(request, 'ana_menu_2.html',)
        num_tipi=tipi.objects.all().count()
        num_bolum=bolum.objects.all().count()
        num_detay=detay.objects.all().count()

        num_grup=grup.objects.all().count()
        num_sirket=sirket.objects.all().count()
        num_musteri=musteri.objects.count()

        return render(request, 'ana_menu_eski.html',
            context={
                'num_tipi':num_tipi,
                'num_bolum':num_bolum,
                'num_detay':num_detay,

                'num_grup': num_grup,
                'num_sirket': num_sirket,
                'num_musteri': num_musteri,
                },
            )

#------------------------------------------------------------------------------

"""
@login_required
def index_ilk(request):
    kisi = request.user
    print("kisi", kisi)
    kullanici = Profile.objects.get(user=kisi)
    print("kullanıcı", kullanici)
#    return redirect('denetim_bolum_sec' )
"""



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
    musteri = denetim_obj.musteri
    denetci = denetim_obj.denetci
    tipi = denetim_obj.tipi
    yaratim_tarihi = denetim_obj.yaratim_tarihi
    yaratan = denetim_obj.yaratan
    hedef_baslangic = denetim_obj.hedef_baslangic
    hedef_bitis = denetim_obj.hedef_bitis
    gerc_baslangic = denetim_obj.gerc_baslangic
    gerc_bitis = denetim_obj.gerc_bitis
    durum = denetim_obj.durum
    gozlemci_obj = gozlemci.objects.filter(denetim=pk)
    i = 0
    g = []
    for gozlem in gozlemci_obj:
        g.append(gozlem.gozlemci)
        i = i + 1
    print("g listesi..", g)
    d = collections.defaultdict(list)
    bolum_obj = sonuc_bolum.objects.filter(denetim=pk)
    for bolum in bolum_obj:
        print("bolum list . bolum", bolum.bolum)
        detay_obj = sonuc.objects.filter(denetim=pk, bolum=bolum.bolum)
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
                'g': g,
               'denetim_adi': denetim_adi,
               'musteri' : musteri,
               'denetci' : denetci,
               'tipi' : tipi,
               'yaratim_tarihi' : yaratim_tarihi,
               'yaratan' : yaratan,
               'hedef_baslangic' : hedef_baslangic,
               'hedef_bitis' : hedef_bitis,
               'durum' : durum,
               }
    return render(request, 'ana_menu_2.html', context )



#--------------------------------------------------------------------------------

@login_required
def denetim_baslat(request, pk=None):

    denetim_no = request.session.get('denetim_no')
    denetim_obj = denetim.objects.get(id=denetim_no)
    print("seçilen denetim", denetim_obj)

    denetim_adi = denetim_obj.denetim_adi
    musteri = denetim_obj.musteri
    yaratim_tarihi = denetim_obj.yaratim_tarihi

    hedef_baslangic = denetim_obj.hedef_baslangic
    hedef_bitis = denetim_obj.hedef_bitis

    context = {'denetim_adi': denetim_adi,
               'musteri' : musteri,
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
    denetim_obj.durum = "C"
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

    devameden_denetimler = denetim.objects.filter(durum="C")
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
            print ("denetim ", dd_denetim)
            dd_konu = request.POST.get('konu', "")
            print ("konu", dd_konu)
            dd_aciklama = request.POST.get('aciklama', "")
            print ("aciklama", dd_aciklama)
            # veri tabanına yazıyor
            acil_obj, created = acil.objects.get_or_create(denetim=dd_denetim)

            if created:
                # means you have created a new db objects
                print("id", acil_obj.id)
                print("denetim", acil_obj.denetim)
                kaydetme_obj = acil(denetim_id=acil_obj.denetim, konu=dd_konu, aciklama=dd_aciklama)
                kaydetme_obj.save()
            else:
                # just refers to the existing one
                print("id", acil_obj.id)
                print("denetim", acil_obj.denetim)
                kaydetme_obj = acil(id=acil_obj.id, denetim_id=acil_obj.denetim, konu=dd_konu, aciklama=dd_aciklama)
                kaydetme_obj.save()


            denetim_no = acil_obj.denetim
            denetim_obj = denetim.objects.get(id=denetim_no)
            denetci = denetim_obj.denetci
            gozlemci_obj = gozlemci.objects.filter(denetim=denetim_no)
            #email işlemi.................
            connection = mail.get_connection()
            connection.open()
            email1 = mail.EmailMessage(
                dd_konu,
                dd_aciklama,
                settings.EMAIL_HOST_USER,
                [denetci.email],
                connection=connection,
                )
            email1.send() # Send the email

            for gozlem in gozlemci_obj:
                email2 = mail.EmailMessage(
                dd_konu,
                dd_aciklama,
                settings.EMAIL_HOST_USER,
                [gozlem.gozlemci.email],
                connection=connection,
                )
            email2.send() # Send the email
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
    denetim_obj.durum = "D"
    denetim_obj.save()
    return redirect('devam_liste' )


#--------------------------------------------------------------------------------

# acil bildirim işlemleri....

@login_required
def acil_bildirim(request, pk=None):

    denetim_no = request.session.get('denetim_no')
    denetim_obj = denetim.objects.get(id=pk)
    print("seçilen denetim kesin ...", denetim_obj)
    denetim_obj.durum = "D"
    denetim_obj.save()
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
            detaylar = sonuc.objects.filter(denetim=denetim_no).filter(bolum=bolum)
            if not detaylar:
                messages.success(request, 'Seçili bölümde bölüm detayı yok....')
                return redirect('denetim_baslat')
            form = DetayForm(denetim_no=denetim_no, secili_bolum=secili_bolum)
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
        ilk_detaylar = sonuc.objects.filter(denetim=denetim_no)
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
        bir = sonuc.objects.filter(denetim=denetim_no)
        iki = bir.filter(bolum=secili_bolum)
        bulunan = iki.get(detay=secili_detay)
        #bulunan = get_object_or_404(sonuc, detay=secili_detay)
        form = SonucForm(request.POST or None, request.FILES or None, instance=bulunan)

        if form.is_valid():
            print("neyse ki valid..bin...ext...")
            # bu detay için tamamı E yap, yani tamamlandı....sonra update yap...
            edit = form.save(commit=False)
            edit.tamam = "E"
            resim_obj = kucukresim.objects.get(kullanici=request.user.id)
            kucuk_resim = resim_obj.foto_kucuk
            edit.foto = kucuk_resim
            edit.save()
            print("kaydetmiş olması lazım.................")

            # bir sonraki................
            # için  işlem yap................
            ilk_detaylar = sonuc.objects.filter(denetim=denetim_no)
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
            form = SonucForm()
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
        ilk_detaylar = sonuc.objects.filter(denetim=denetim_no)
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
        print("secili - detay.... bakalım  doğru mu...", secili_detay)
        request.session['secili_detay'] = secili_detay
        form = SonucForm()
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
            sonuc_list = sonuc.objects.filter(denetim=denetim_no).order_by('bolum')
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
# gözlemci seçimi ile ilgili bölüm.....
# önce denetim seçiliyor...

@login_required
def gozlemci_denetim_sec(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = IlkDenetimSecForm(request.POST, kullanan=kullanan, durum="A")
        print("denetimi seçti gözlemci seçimi için...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            denetim_no = request.POST.get('denetim_no', "")
            print ("denetim_no", denetim_no)
            request.session['ilk_secili_denetim'] = denetim_no
            #form = GozlemciForm()
            return redirect('gozlemci_sec_devam')
            #return render(request, 'islem/gozlemci_sec_devam.html', {'form': form,})
        else:
            print(" nah valid............")
            return render(request, 'islem/gozlemci_denetim_sec.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        #ilk_secili_denetim = request.session.get('ilk_secili_denetim')
        kullanan = request.user.id
        print("kullanan  ..", kullanan)
        form = IlkDenetimSecForm(kullanan=kullanan, durum="A")
        return render(request, 'islem/gozlemci_denetim_sec.html', {'form': form,})

#-------------------------------------------------------------------------------

@login_required
def gozlemci_sec_devam(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GozlemciForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            denetim_no = request.session.get('ilk_secili_denetim')
            kisi_list = request.POST.getlist('kisi', "")
            print ("kisi_list...:", kisi_list, len(kisi_list))
            if len(kisi_list)!=0:
                silme_obj = gozlemci.objects.filter(denetim=denetim_no)
                silme_obj.delete()

            i = 0
            while i < len(kisi_list):
                print(kisi_list[i])
                kaydetme_obj = gozlemci(denetim_id=denetim_no,
                                        gozlemci_id=kisi_list[i],
                                        )
                kaydetme_obj.save()
                i = i + 1

            if (i!=0):
                messages.success(request, 'Başarıyla kaydetti....')
            return redirect('index')
        else:
            print("gözlemci seç devam ...valid değil....")
            return render(request, 'islem/gozlemci_sec_devam.html', {'form': form,})

    # if a GET (or any other method) we'll create a blank form
    else:
        #selected_alt = request.session.get('selected_alt')
        form = GozlemciForm()
        return render(request, 'islem/gozlemci_sec_devam.html', {'form': form,})



#------------------------------------------------------------------------------
# bölüm seçimi ile ilgili bölüm.....
# önce denetim seçiliyor...

@login_required
def bolum_denetim_sec(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = IlkDenetimSecForm(request.POST, kullanan=kullanan, durum="A")
        print("denetimi seçti gözlemci seçimi için...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            denetim_no = request.POST.get('denetim_no', "")
            print ("denetim_no", denetim_no)
            request.session['ilk_secili_denetim'] = denetim_no
            #form = GozlemciForm()
            return redirect('bolum_sec_devam')
            #return render(request, 'islem/gozlemci_sec_devam.html', {'form': form,})
        else:
            print(" nah valid............")
            return render(request, 'islem/bolum_denetim_sec.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        #ilk_secili_denetim = request.session.get('ilk_secili_denetim')
        kullanan = request.user.id
        print("kullanan  ..", kullanan)
        form = IlkDenetimSecForm(kullanan=kullanan, durum="A")
        return render(request, 'islem/bolum_denetim_sec.html', {'form': form,})


#-------------------------------------------------------------------------------

@login_required
def bolum_sec_devam(request, pk=None):
    # if this is a POST request we need to process the form data
    denetim_no = request.session.get('ilk_secili_denetim')
    denetim_obj = denetim.objects.get(id=denetim_no)
    denetim_tipi = denetim_obj.tipi
    print("seçili denetim...", denetim_no, "denetim tipi...", denetim_tipi)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = IlkBolumForm(request.POST, denetim_tipi=denetim_tipi, denetim_no=denetim_no)
        # check whether it's valid:
        if form.is_valid():
            bolum_list = request.POST.getlist('bolum', "")
            print ("bolum_list...:", bolum_list, len(bolum_list))
            yeni_list = []
            if len(bolum_list) == 0:
                yeni_list = []
            else:
                for x in bolum_list:
                    yeni_list.append(x)

            print("yeni list bölüm listten aktarılan...", yeni_list)

            #if len(bolum_list)!=0:
            #    silme_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
            #    silme_obj.delete()

            # sonuç bölüm dosyasındaki eski tüm kayıtları önce temizle....
            silme_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
            eski_list = []
            for secili_bolum in silme_obj:
                eski_list.append(secili_bolum.bolum.id)
            print ("eski_list...:", eski_list, len(eski_list))
            yeni_set = set(yeni_list)
            print("yeni set...:", yeni_set)

            silme_list = []
            if len(yeni_list) == 0:
                silme_list = eski_list
            else:
                i = 0
                for x in eski_list:
                    if str(x) in yeni_set:
                        print("yaptın onu.....")
                        pass
                    else:
                        print("eski listte bölüm listesinde değil..:", x , "yeni list", yeni_list)
                        silme_list.append(x)
                    i = i + 1

            print("işte çıkartılacak bölümler...", silme_list, len(silme_list))
            silme_obj.delete()
            i = 0
            while i < len(silme_list):
                print(silme_list[i])
                detay_sil_obj = sonuc.objects.filter(denetim_id=denetim_no).filter(bolum=silme_list[i])
                detay_sil_obj.delete()
                i = i + 1
            # sonra bastan kaydet....sonuc bölüm dosyasındaki denetim kayıtlarını...
            i = 0
            while i < len(bolum_list):
                print(bolum_list[i])
                kaydetme_obj = sonuc_bolum(denetim_id=denetim_no,
                                           bolum_id=bolum_list[i],
                                           )
                kaydetme_obj.save()
                i = i + 1

            #if (i!=0):
            messages.success(request, 'Kaydetti....')
            return redirect('index')
        else:
            print("bölüm seç devam ...valid değil....")
            return render(request, 'islem/bolum_sec_devam.html', {'form': form,})

    # if a GET (or any other method) we'll create a blank form
    else:
        #selected_alt = request.session.get('selected_alt')
        form = IlkBolumForm(denetim_tipi=denetim_tipi, denetim_no=denetim_no)
        return render(request, 'islem/bolum_sec_devam.html', {'form': form,})


#------------------------------------------------------------------------------
# detay seçimi ile ilgili bölüm.....
# önce denetim seçiliyor...

@login_required
def detay_denetim_sec(request, pk=None):
    # if this is a POST request we need to process the form data
    kullanan = request.user.id
    print("kullanan  ..", kullanan)
    denetim_no = request.session.get('detay_icin_bolum')
    print("denetim no..", denetim_no)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = IkiliSecForm(request.POST, kullanan=kullanan, denetim_no=denetim_no)
        print("ikiliyi secti....")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            dd_denetim_no = request.POST.get('denetim', "")
            dd_bolum_no = request.POST.get('bolum', "")
            print("denetim no - valid sonrası ", dd_denetim_no)
            print("bolum no - valid sonrası", dd_bolum_no)
            request.session['ikili_secili_denetim'] = dd_denetim_no
            request.session['ikili_secili_bolum'] = dd_bolum_no
            #form = GozlemciForm()
            return redirect('detay_sec_devam')
            #return render(request, 'islem/gozlemci_sec_devam.html', {'form': form,})
        else:
            print(" olmadı valid............")
            return render(request, 'islem/detay_denetim_sec.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        #ilk_secili_denetim = request.session.get('ilk_secili_denetim')

        form = IkiliSecForm(kullanan=kullanan, denetim_no=denetim_no)
        return render(request, 'islem/detay_denetim_sec.html', {'form': form,})


#-------------------------------------------------------------------------------

@login_required
def detay_sec_devam(request, pk=None):
    # if this is a POST request we need to process the form data
    denetim_no = request.session.get('ikili_secili_denetim')
    sonuc_bolum_no = request.session.get('ikili_secili_bolum')
    print("seçili denetim...", denetim_no)
    print("secili sonuç-bölüm...", sonuc_bolum_no)
    bol_obj = sonuc_bolum.objects.get(id=sonuc_bolum_no)
    bolum_no = bol_obj.bolum.id
    print("seçili bölüm...", bolum_no)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = IlkDetayForm(request.POST, bolum_no=bolum_no)
        # check whether it's valid:
        if form.is_valid():
            detay_list = request.POST.getlist('detay', "")
            print ("detay_list...:", detay_list, len(detay_list))

            if len(detay_list)!=0:
                silme_obj = sonuc.objects.filter(denetim=denetim_no).filter(bolum=bolum_no)
                silme_obj.delete()

            i = 0
            while i < len(detay_list):
                print("detay-list-i", detay_list[i])
                detay_no = int(detay_list[i])
                print("işte detay no...", detay_no)
                kaydetme_obj = sonuc(denetim_id=denetim_no,
                                     bolum_id=bolum_no,
                                     detay_id=detay_no,
                                     )
                kaydetme_obj.save()
                i = i + 1

            if (i!=0):
                messages.success(request, 'Başarıyla kaydetti....')
            return redirect('index')
        else:
            print("bölüm seç devam ...valid değil....")
            return render(request, 'islem/detay_sec_devam.html', {'form': form,})

    # if a GET (or any other method) we'll create a blank form
    else:
        #selected_alt = request.session.get('selected_alt')
        form = IlkDetayForm(bolum_no=bolum_no)
        return render(request, 'islem/detay_sec_devam.html', {'form': form,})


#------------------------------------------------------------------------------
# iş emri oluşturma ile ilgili bölüm.....
# önce denetim seçiliyor...

@login_required
def isemri_denetim_sec(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = IlkDenetimSecForm(request.POST, kullanan=kullanan, durum="A")
        print("denetimi seçti işemri oluşturma için...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            denetim_no = request.POST.get('denetim_no', "")
            print ("denetim_no", denetim_no)
            request.session['ilk_secili_denetim'] = denetim_no
            #form = GozlemciForm()
            #return redirect('isemri_olustur_devam')
            return redirect('isemri_olustur_devam')
            #return render(request, 'islem/gozlemci_sec_devam.html', {'form': form,})
        else:
            print(" nah valid............")
            return render(request, 'islem/isemri_denetim_sec.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        #ilk_secili_denetim = request.session.get('ilk_secili_denetim')
        kullanan = request.user.id
        print("kullanan  ..", kullanan)
        form = IlkDenetimSecForm(kullanan=kullanan, durum="A")
        return render(request, 'islem/isemri_denetim_sec.html', {'form': form,})


#-------------------------------------------------------------------------------
from .models import gozlemci

@login_required
def isemri_olustur_devam(request, pk=None):
    denetim_no = request.session.get('ilk_secili_denetim')
    print("seçili denetim...", denetim_no)
    #gozlemci = ""
    bol_varmi = sonuc_bolum.objects.filter(denetim=denetim_no)
    print("bölümler", bol_varmi)
    det_varmi = sonuc.objects.filter(denetim=denetim_no)
    print("detaylar", det_varmi)
    goz_varmi = gozlemci.objects.filter(denetim=denetim_no)
    print("gözlemciler", goz_varmi)

    if not(goz_varmi):
        messages.success(request, 'Gözlemci girilmemiş....')
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
    musteri = denetim_obj.musteri
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
    gozlemci_obj = gozlemci.objects.filter(denetim=denetim_no)
    i = 0
    g = []
    for gozlem in gozlemci_obj:
        g.append(gozlem.gozlemci)
        i = i + 1
    print("g list...",g)
    # bölüm ve detay listesi..........................
    d = collections.defaultdict(list)
    bolum_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
    for bolum in bolum_obj:
        print("bolum list . bolum", bolum.bolum)
        detay_obj = sonuc.objects.filter(denetim=denetim_no, bolum=bolum.bolum)
        for detay in detay_obj:
            print("detay list . detay", detay.bolum, detay.detay)
            d[detay.bolum].append(detay.detay)
    print("***********************")
    print(d)
    d.default_factory = None
    dict_bol_detay = dict(d)
    gozgoz = g
    print("************************")
    print(dict_bol_detay)
    print(gozgoz)
    context = {'dict_bol_detay':dict_bol_detay,
               'gozgoz': gozgoz,
               'denetim_adi': denetim_adi,
               'musteri' : musteri,
               'denetci' : denetci,
               'tipi' : tipi,
               'yaratim_tarihi' : yaratim_tarihi,
               'yaratan' : yaratan,
               'hedef_baslangic' : hedef_baslangic,
               'hedef_bitis' : hedef_bitis,
               'durum' : durum,
               }
    return render(request, 'islem/isemri_olustur_devam.html', context )





#-------------------------------------------------------------------
from django.core import mail

@login_required
def isemri_yarat(request, pk=None):
    # if this is a POST request we need to process the form data
    denetim_no = request.session.get('ilk_secili_denetim')
    print("seçili denetim...", denetim_no)
    # e-mailleri at..............
    denetim_obj = denetim.objects.get(id=denetim_no)
    print("seçilen denetim", denetim_obj)
    denetci = denetim_obj.denetci
    gozlemci_obj = gozlemci.objects.filter(denetim=denetim_no)
    if not(gozlemci_obj):
        messages.success(request, 'Gözlemci girilmemiş....')
        return redirect('isemri_denetim_sec')
#email işlemi.................
    connection = mail.get_connection()
    connection.open()
    email1 = mail.EmailMessage(
        'denetçi',
        'denetçi oldunuz....',
        settings.EMAIL_HOST_USER,
        [denetci.email],
        connection=connection,
        )
    email1.send() # Send the email

    for gozlem in gozlemci_obj:
        email2 = mail.EmailMessage(
            'gözlemci',
            'gözlemci oldunuz...',
            settings.EMAIL_HOST_USER,
            [gozlem.gozlemci.email],
            connection=connection,
            )
        email2.send() # Send the email
    connection.close()
    # email işlemi sonu.....................

    denetim_obj.durum = "B"
    denetim_obj.save()
    messages.success(request, 'Başarıyla oluşturuldu....')
    return redirect('index')



#------------------------------------------------------------------------------
# işemri sonrası denetim seçimi ile ilgili bölüm.....
# önce denetim seçiliyor...

@login_required
def isemrisonrasi_sec(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = IlkDenetimSecForm(request.POST, kullanan=kullanan, durum="B")
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
    det_varmi = sonuc.objects.filter(denetim=denetim_no)
    print("detaylar", det_varmi)
    goz_varmi = gozlemci.objects.filter(denetim=denetim_no)
    print("gözlemciler", goz_varmi)

    if not(goz_varmi):
        messages.success(request, 'Gözlemci girilmemiş....')
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
    musteri = denetim_obj.musteri
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
    gozlemci_obj = gozlemci.objects.filter(denetim=denetim_no)
    i = 0
    g = []
    for gozlem in gozlemci_obj:
        g.append(gozlem.gozlemci)
        i = i + 1
    print("g list...",g)
    # bölüm ve detay listesi..........................
    d = collections.defaultdict(list)
    bolum_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
    for bolum in bolum_obj:
        print("bolum list . bolum", bolum.bolum)
        detay_obj = sonuc.objects.filter(denetim=denetim_no, bolum=bolum.bolum)
        for detay in detay_obj:
            print("detay list . detay", detay.bolum, detay.detay)
            d[detay.bolum].append(detay.detay)
    print("***********************")
    print(d)
    d.default_factory = None
    dict_bol_detay = dict(d)
    gozgoz = g
    print("************************")
    print(dict_bol_detay)
    print(gozgoz)
    context = {'dict_bol_detay':dict_bol_detay,
               'gozgoz': gozgoz,
               'denetim_adi': denetim_adi,
               'musteri' : musteri,
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
        form = IlkDenetimSecForm(request.POST, kullanan=kullanan, durum="C")
        print("denetimi seçti gözlemci seçimi için...")
        # check whether it's valid:            denetim_obj.hedef_baslangic = yeni_baslangic

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
        form = IlkDenetimSecForm(kullanan=kullanan, durum="C")
        return render(request, 'islem/baslanmislar_denetim_sec.html', {'form': form,})

#-------------------------------------------------------------------------------

@login_required
def baslanmislar_devam(request, pk=None):
    denetim_no = request.session.get('ilk_secili_denetim')
    print("iş emri sonrası devam....seçili denetim...", denetim_no)
    #gozlemci = ""
    bol_varmi = sonuc_bolum.objects.filter(denetim=denetim_no)
    print("bölümler", bol_varmi)
    det_varmi = sonuc.objects.filter(denetim=denetim_no)
    print("detaylar", det_varmi)
    goz_varmi = gozlemci.objects.filter(denetim=denetim_no)
    print("gözlemciler", goz_varmi)

    if not(goz_varmi):
        messages.success(request, 'Gözlemci girilmemiş....')
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
    musteri = denetim_obj.musteri
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
    gozlemci_obj = gozlemci.objects.filter(denetim=denetim_no)
    i = 0
    g = []
    for gozlem in gozlemci_obj:
        g.append(gozlem.gozlemci)
        i = i + 1
    print("g list...",g)
    # bölüm ve detay listesi..........................
    d = collections.defaultdict(list)
    bolum_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
    for bolum in bolum_obj:
        print("bolum list . bolum", bolum.bolum)
        detay_obj = sonuc.objects.filter(denetim=denetim_no, bolum=bolum.bolum)
        for detay in detay_obj:
            print("detay list . detay", detay.bolum, detay.detay)
            d[detay.bolum].append(detay.detay)
    print("***********************")
    print(d)
    d.default_factory = None
    dict_bol_detay = dict(d)
    gozgoz = g
    print("************************")
    print(dict_bol_detay)
    print(gozgoz)
    context = {'dict_bol_detay':dict_bol_detay,
               'gozgoz': gozgoz,
               'denetim_adi': denetim_adi,
               'musteri' : musteri,
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
        form = MusteriSecForm(request.POST)
        print("denetimi seçti gözlemci seçimi için...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            musteri = request.POST.get('musteri', "")
            print ("musteri", musteri)
            request.session['secili_musteri'] = musteri
            #form = GozlemciForm()
            return redirect('sonlandirilan_devam')
            #return render(request, 'islem/gozlemci_sec_devam.html', {'form': form,})
        else:
            print(" nah valid............")
            return render(request, 'islem/sonlandirilan_musteri_sec.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        #ilk_secili_denetim = request.session.get('ilk_secili_denetim')
        kullanan = request.user.id
        print("kullanan  ..", kullanan)
        form = MusteriSecForm()
        return render(request, 'islem/sonlandirilan_musteri_sec.html', {'form': form,})

#-------------------------------------------------------------------------------

@login_required
def sonlandirilan_devam(request, pk=None):
    secili_musteri = request.session.get('secili_musteri')
    musteri_no = int(secili_musteri)
    print("seçili musteri...", secili_musteri, "musteri no..:", musteri_no)
    musteri_obj = musteri.objects.get(id=musteri_no)
    #sonlandirilan_denetim_obj = denetim.objects.filter(musteri=secili_musteri).filter(durum="D")
    sonlandirilan_denetim_obj = denetim.objects.filter(musteri=secili_musteri)
    context = {'sonlandirilan_denetim_obj':sonlandirilan_denetim_obj,
               'musteri_obj': musteri_obj,
               }
    return render(request, 'islem/sonlandirilan_denetim_list.html', context )


#-------------------------------------------------------------------------------

@login_required
def sonlandirilan_ilerle(request, pk=None):
    denetim_no = pk
    request.session['secilen_denetim'] = denetim_no
    sonuc_list = sonuc.objects.filter(denetim=denetim_no).order_by('bolum')
    denetimin_adi = sonuc_list.first().denetim.denetim_adi
    denetimin_durumu = sonuc_list.first().denetim.durum
    context = {'sonuc_list': sonuc_list, 'denetimin_adi': denetimin_adi, 'denetimin_durumu': denetimin_durumu}
    return render(request, 'islem/sonlandirilan_detay_list.html', context)


"""
# iptal edildi değiştirildi....
def sonlandirilan_devam_iptal(request, pk=None):
    denetim_no = request.session.get('ilk_secili_denetim')
    #gozlemci = ""
    bol_varmi = sonuc_bolum.objects.filter(denetim=denetim_no)
    print("bölümler", bol_varmi)
    det_varmi = sonuc.objects.filter(denetim=denetim_no)
    print("detaylar", det_varmi)
    goz_varmi = gozlemci.objects.filter(denetim=denetim_no)
    print("gözlemciler", goz_varmi)

    if not(goz_varmi):
        messages.success(request, 'Gözlemci girilmemiş....')
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
    musteri = denetim_obj.musteri
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
    gozlemci_obj = gozlemci.objects.filter(denetim=denetim_no)
    i = 0
    g = []
    for gozlem in gozlemci_obj:
        g.append(gozlem.gozlemci)
        i = i + 1
    print("g list...",g)
    # bölüm ve detay listesi..........................
    d = collections.defaultdict(list)
    bolum_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
    for bolum in bolum_obj:
        print("bolum list . bolum", bolum.bolum)
        detay_obj = sonuc.objects.filter(denetim=denetim_no, bolum=bolum.bolum)
        for detay in detay_obj:
            print("detay list . detay", detay.bolum, detay.detay)
            d[detay.bolum].append(detay.detay)
    print("***********************")
    print(d)
    d.default_factory = None
    dict_bol_detay = dict(d)
    gozgoz = g
    print("************************")
    print(dict_bol_detay)
    print(gozgoz)
    context = {'dict_bol_detay':dict_bol_detay,
               'gozgoz': gozgoz,
               'denetim_adi': denetim_adi,
               'musteri' : musteri,
               'denetci' : denetci,
               'tipi' : tipi,
               'yaratim_tarihi' : yaratim_tarihi,
               'yaratan' : yaratan,
               'hedef_baslangic' : hedef_baslangic,
               'hedef_bitis' : hedef_bitis,
               'durum' : durum,
               }
    return render(request, 'islem/isemri_olustur_devam.html', context )
"""


#------------------------------------------------------------------    denetim_no = request.session.get('ilk_secili_denetim')--
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

# denetçi değiştiriliyor...

@login_required
def denetci_degistir(request, pk=None):
    denetim_no = request.session.get('ilk_secili_denetim')
    denetim_obj = denetim.objects.get(id=denetim_no)
    print("seçilen denetim kesin ...", denetim_obj)
    denetci = denetim_obj.denetci
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = YeniDenetciSecForm(request.POST, denetci=denetci)
        print("yeni denetci secimi için...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            yeni_denetci = request.POST.get('yeni_denetci', "")
            print ("yeni denetci", yeni_denetci)
            print ("eski denetci", denetci)
            yenidenetci_obj = User.objects.get(id=yeni_denetci)
            denetci_obj = User.objects.get(username=denetci)
            print("yeni denetçi obj....", yenidenetci_obj)
            print("eski denetçi obj....", denetci_obj)
            #email işlemi.................
            connection = mail.get_connection()
            connection.open()
            email1 = mail.EmailMessage(
                'yeni_denetci',
                'denetçi oldunuz....',
                settings.EMAIL_HOST_USER,
                [yenidenetci_obj.email],
                connection=connection,
                )
            email1.send() # Send the email

            email2 = mail.EmailMessage(
                'denetci',
                'denetçiliğiniz kaldırıldı....',
                settings.EMAIL_HOST_USER,
                [denetci_obj.email],
                connection=connection,
                )
            email1.send() # Send the email
            connection.close()
            # email işlemi sonu.....................
            denetim_obj.denetci_id = yeni_denetci
            denetim_obj.save()
            messages.success(request, 'Yeni denetçi atandı....')
            return redirect('index' )
        else:
            print(" nah valid............")
            return render(request, 'islem/yeni_denetci_gir.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        #ilk_secili_denetim = request.session.get('ilk_secili_denetim')
        kullanan = request.user.id
        print("kullanan  ..", kullanan)
        form = YeniDenetciSecForm(denetci=denetci)
        return render(request, 'islem/yeni_denetci_gir.html', {'form': form,})


#--------------------------------------------------------------------------------

# tarih  değiştiriliyor...

@login_required
def tarih_degistir(request, pk=None):
    denetim_no = request.session.get('ilk_secili_denetim')
    denetim_obj = denetim.objects.get(id=denetim_no)
    denetci = denetim_obj.denetci
    gozlemci_obj = gozlemci.objects.filter(denetim=denetim_no)
    print("seçilen denetim kesin ...", denetim_obj)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        form = YeniTarihForm(request.POST)
        print("yeni tarih için...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            yeni_baslangic = request.POST.get('hedef_baslangic', "")
            yeni_bitis = request.POST.get('hedef_bitis', "")
            print ("yeni baslangic", yeni_baslangic)
            print ("yeni bitiş", yeni_bitis)
            #email işlemi.................
            connection = mail.get_connection()
            connection.open()
            email1 = mail.EmailMessage(
                'yeni_tarih',
                'denetim tarihi değişti....',
                settings.EMAIL_HOST_USER,
                [denetci.email],
                connection=connection,
                )

            email1.send() # Send the email

            for gozlem in gozlemci_obj:
                email2 = mail.EmailMessage(
                'yeni tarih ',
                'denetim tarihi değişti...',
                settings.EMAIL_HOST_USER,
                [gozlem.gozlemci.email],
                connection=connection,
                )
            email2.send() # Send the email
            connection.close()
            # email işlemi sonu.....................
            denetim_obj.hedef_baslangic = yeni_baslangic
            denetim_obj.hedef_bitis = yeni_bitis
            denetim_obj.save()
            messages.success(request, 'Yeni tarihler kaydedildi....')
            return redirect('index' )

        else:
            print(" nah valid............")
            return render(request, 'islem/yeni_tarih_gir.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        #ilk_secili_denetim = request.session.get('ilk_secili_denetim')
        kullanan = request.user.id
        print("kullanan  ..", kullanan)
        form = YeniTarihForm()
        return render(request, 'islem/yeni_tarih_gir.html', {'form': form,})

#--------------------------------------------------------------------------------

# tarih  değiştiriliyor...

@login_required
def deneme_filteredselectmultiple(request, pk=None):
    denetim_no = request.session.get('ilk_secili_denetim')
    denetim_obj = denetim.objects.get(id=denetim_no)
    durum = denetim_obj.durum
    denetci = denetim_obj.denetci
    gozlemci_obj = gozlemci.objects.filter(denetim=denetim_no)
    print("seçilen denetim kesin ...", denetim_obj)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        kullanan = request.user.id
        #form = MyForm(request.POST, kullanan=kullanan, durum=durum)
        form = MyForm(request.POST)
        print("yeni tarih için...")
        # check whether it's valid:
        if form.is_valid():
            print("valid....")
            yeni_baslangic = request.POST.get('hedef_baslangic', "")
            yeni_bitis = request.POST.get('hedef_bitis', "")
            print ("yeni baslangic", yeni_baslangic)
            print ("yeni bitiş", yeni_bitis)
            #email işlemi.................
            messages.success(request, 'deneme başarılı....')
            return redirect('index' )
            #return render(request, 'islem/gozlemci_sec_devam.html', {'form': form,})
        else:
            print(" nah valid............")
            return render(request, 'islem/yeni_tarih_gir.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        #ilk_secili_denetim = request.session.get('ilk_secili_denetim')
        kullanan = request.user.id
        print("kullanan  ..", kullanan)
        #form = MyForm(kullanan=kullanan, durum=durum)
        form = MyForm()
        return render(request, 'islem/deneme_filteredselectmultiple.html', {'form': form,})



#--------------------------------------------------------------------


def denetim_bolum_js(request, pk=None):
    print("selam buraya geldik...denetim bölüm js")
    print("User.id.....:", request.user.id)
    kullanan = request.user.id
    response_data ={}
    if request.method == 'GET':
        selected = request.GET.get('selected', None)
        print("selected...:", selected,)
        request.session['detay_icin_bolum'] = selected
    print ("son nokta denetim bölüm js.....", response_data)
    return HttpResponse(response_data, content_type='application/json')



#---------------------------------------------------------------------

@login_required
def denetim_sil(request, pk=None):
    print("denetim sildeki pk:", pk)
    object = get_object_or_404(denetim, pk=pk)
    sil_denetim = object.denetim_adi
    sil_id = object.id
    print("sil_denetim", sil_denetim)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_denetim': sil_denetim, 'pk': pk,}
    return render(request, 'islem/denetim_sil_soru.html', args)


@login_required
def denetim_sil_kesin(request, pk=None):
    print("denetim sil kesindeki pk:", pk)
    object = denetim.objects.get(id=pk)
    object.durum = "X"
    object.save()
#********************************************************
#....  ilgili kişilere e-posta gönder...burada yok......
#.........................................................
    messages.success(request, 'Başarıyla silindi....')
    return redirect('denetim')

#------------------------------------------------------------------------------





@login_required
def tipi_sil(request, pk=None):
    print("tip sildeki pk:", pk)
    object = get_object_or_404(tip, pk=pk)
    sil_tip = object.tip_adi
    sil_id = object.id
    print("sil_tip", sil_tip)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_tip': sil_tip, 'pk': pk,}
    return render(request, 'islem/tipi_sil_soru.html', args)


@login_required
def tipi_sil_kesin(request, pk=None):
    print("tip sil kesindeki pk:", pk)
    object = get_object_or_404(tip, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('tipi')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('tipi')

    subject = 'konusu bu'
    from_email = settings.EMAIL_HOST_USER
    to_email = ['lvengin@yahoo.com', 'lvengin@gmail.com']
    email_message = ' ilk deneme bu .....'
    send_mail(subject,
              email_message,
              from_email,
              to_email,
              fail_silently=False)

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
def musteri_sil(request, pk=None):
    print("musteri sildeki pk:", pk)
    object = get_object_or_404(musteri, pk=pk)
    sil_musteri = object.musteri_adi
    sil_id = object.id
    print("sil_musteri", sil_musteri)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_musteri': sil_musteri, 'pk': pk,}
    return render(request, 'islem/musteri_sil_soru.html', args)


@login_required
def musteri_sil_kesin(request, pk=None):
    print("musteri sil kesindeki pk:", pk)
    object = get_object_or_404(musteri, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('musteri')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('musteri')


#  .............................................................
#  denetim yaratma işlemleri ...................................
# ..............................................................



@login_required
def denetim_create(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Denetim_BForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            dd_denetim_adi = request.POST.get('denetim_adi', "")
            dd_musteri = request.POST.get('musteri', "")
            dd_denetci = request.POST.get('denetci', "")
            dd_tipi = request.POST.get('tipi', "")
            dd_hedef_baslangic = request.POST.get('hedef_baslangic', "")
            dd_hedef_bitis = request.POST.get('hedef_bitis', "")
            dd_aciklama = request.POST.get('aciklama', "")
            #if (dd_hedef_baslangic > dd_hedef_bitis):
            # put controls here if necessary..........
            kaydetme_obj = denetim(denetim_adi=dd_denetim_adi,
                                    musteri_id=dd_musteri,
                                    denetci_id=dd_denetci,
                                    tipi_id=dd_tipi,
                                    hedef_baslangic=dd_hedef_baslangic,
                                    hedef_bitis=dd_hedef_bitis,
                                    yaratan_id=request.user.id,
                                    durum="A"
                                    )
            kaydetme_obj.save()
            messages.success(request, 'Başarıyla kaydetti....')
            return redirect('denetim_create')
        else:
            #messages.success(request, 'Formda uygunsuzluk var....')
            #return redirect('denetim_create')
            return render(request, 'islem/denetim_form.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        #selected_alt = request.session.get('selected_alt')
        form = Denetim_BForm()
        return render(request, 'islem/denetim_form.html', {'form': form,})


class DenetimUpdate(LoginRequiredMixin,UpdateView):
    model = denetim
    fields = ('denetim_adi', 'musteri', 'denetci', 'tipi', 'hedef_baslangic', 'hedef_bitis', 'aciklama')
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

# musteri yaratma, güncelleme, silme ...

class MusteriCreate(LoginRequiredMixin,CreateView):
    model = musteri
    fields = '__all__'
    success_url = "/islem/musteri/create/"

class MusteriUpdate(LoginRequiredMixin,UpdateView):
    model = musteri
    fields = '__all__'
    success_url = "/islem/musteri/"

class MusteriDelete(LoginRequiredMixin,DeleteView):
    model = musteri
    success_url = reverse_lazy('musteri')


#--------------------------------------------------------------

#????????????????????????????????????????????????????????????


class SonucUpdate(LoginRequiredMixin,UpdateView):
    model = sonuc
    fields = '__all__'
    success_url = "/islem/sonuc/"

#-----------------------------------------?????????????????????????

class SonucListView(LoginRequiredMixin,generic.ListView):
    model = sonuc
    paginate_by = 20

class SonucDetailView(LoginRequiredMixin,generic.DetailView):
    model = sonuc


#------------------------------------------------------------

class TipiListView(LoginRequiredMixin,generic.ListView):
    model = tipi
    #paginate_by = 20

class TipiDetailView(LoginRequiredMixin,generic.DetailView):
    model = tipi

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

class MusteriListView(LoginRequiredMixin,generic.ListView):
    model = musteri

class MusteriDetailView(LoginRequiredMixin,generic.DetailView):
    model = musteri

#------------------------------------------------------------

class DenetimListView(LoginRequiredMixin,generic.ListView):
    queryset = denetim.objects.filter(durum="A")


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
    queryset = denetim.objects.filter(durum="D")
    template_name = "/islem/denetim_sonlandirilan_list.html"

class Denetim_3DetailView(LoginRequiredMixin,generic.DetailView):
    queryset = denetim.objects.filter(durum="D")

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
