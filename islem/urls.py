
from django.views.generic import RedirectView
from django.views.generic import View
from django.conf.urls import include, url
from . import views
from django.utils.translation import gettext as _
from rest_framework import routers, serializers, viewsets
# from django.contrib.auth import views
from django.conf.urls import include
from django.contrib.admin.widgets import FilteredSelectMultiple

from functools import reduce
from itertools import chain
from pickle import PicklingError

from django import forms
from django.core import signing
from django.db.models import Q
from django.forms.models import ModelChoiceIterator
from django.urls import reverse
from django.utils.translation import get_language

from .views import denetimautocomplete, sonucbolumautocomplete, takipciautocomplete, denetciautocomplete
from .views import bolumautocomplete, detayautocomplete, tipiautocomplete, projeautocomplete




urlpatterns = [
    url(r'^$', views.index, name='index'),
    # dal denemesi için..................
    url(r'^denetim-autocomplete/$', denetimautocomplete.as_view(),name='denetim-autocomplete',),
    url(r'^sonucbolum-autocomplete/$', sonucbolumautocomplete.as_view(),name='sonucbolum-autocomplete',),
    url(r'^takipci-autocomplete/$', takipciautocomplete.as_view(),name='takipci-autocomplete',),
    url(r'^bolum-autocomplete/$', bolumautocomplete.as_view(),name='bolum-autocomplete',),
    url(r'^detay-autocomplete/$', detayautocomplete.as_view(),name='detay-autocomplete',),
    url(r'^tipi-autocomplete/$', tipiautocomplete.as_view(),name='tipi-autocomplete',),
    url(r'^proje-autocomplete/$', projeautocomplete.as_view(),name='proje-autocomplete',),
    url(r'^denetci-autocomplete/$', denetciautocomplete.as_view(),name='denetci-autocomplete',),





    #url(r'^gozlemci/$', views.gozlemci_sec, name='gozlemci_sec'),
    url(r'^denetim/(?P<pk>\d+)$', views.denetim_detay, name='denetim_detay'),
    #url(r'^denetim/(?P<pk>\d+)/pdf/$', views.GeneratePDF.as_view(), name='GeneratePDF'),
    url(r'^denetim/(?P<pk>\d+)/pdf/$', views.generate_pdf, name='generate_pdf'),
    url(r'^baslat/$', views.denetim_baslat, name='denetim_baslat'),
    url(r'^baslat/kesin/$', views.denetim_baslat_kesin, name='denetim_baslat_kesin'),
    url(r'^devam/(?P<pk>\d+)$', views.denetim_devam_islemleri, name='denetim_devam_islemleri'),
    url(r'^tekrar/(?P<pk>\d+)$', views.denetim_tekrar_islemleri, name='denetim_tekrar_islemleri'),
    url(r'^tekrar/(?P<pk>\d+)/kesin/$', views.denetim_tekrarla_kesin, name='denetim_tekrarla_kesin'),
    url(r'^tamamla/(?P<pk>\d+)$', views.denetim_tamamla, name='denetim_tamamla'),
    url(r'^acilbildirim/(?P<pk>\d+)$', views.acil_bildirim, name='acil_bildirim'),
    url(r'^tamamla/(?P<pk>\d+)/kesin/$', views.denetim_tamamla_kesin, name='denetim_tamamla_kesin'),
    url(r'^devam_liste/$', views.devam_liste, name='devam_liste'),
    url(r'^acil_devam_sec/$', views.acil_devam_sec, name='acil_devam_sec'),
    url(r'^qrcode/$', views.qrcode_tara, name='qrcode_tara'),
    url(r'^bolum_sec/$', views.denetim_bolum_sec, name='denetim_bolum_sec'),
    url(r'^bolum_sec/secilen_bolumu_kaydet/$', views.secilen_bolumu_kaydet, name='secilen_bolumu_kaydet'),
    url(r'^bolum_sec/detay_islemleri_baslat/$', views.detay_islemleri_baslat, name='detay_islemleri_baslat'),
    url(r'^bolum_sec/denetim_detay_islemleri/$', views.denetim_detay_islemleri, name='denetim_detay_islemleri'),
    url(r'^bolum_sec/denetim_detay_islemleri/kucuk_resim_al/$', views.kucuk_resim_al, name='kucuk_resim_al'),
    url(r'^baslat/devam/secilen_bolumu_kaydet/$', views.secilen_bolumu_kaydet, name='secilen_bolumu_kaydet'),
    url(r'^baslat/devam/detay_islemleri_baslat/$', views.detay_islemleri_baslat, name='detay_islemleri_baslat'),
    url(r'^baslat/devam/denetim_detay_islemleri/$', views.denetim_detay_islemleri, name='denetim_detay_islemleri'),



#-------------------------------------------------------------------------------------------------
    # grup urlleri aşağıda....
    url(r'^deneme/$', views.deneme_denetim, name='deneme_denetim'),
    url(r'^deneme_iki/$', views.deneme_sonucbolum, name='deneme_sonucbolum'),



    url(r'^grup/$', views.GrupListView.as_view(), name='grup'),
    url(r'^grup/(?P<pk>\d+)$', views.GrupDetailView.as_view(), name='grup-detail'),
    url(r'^grup/create/$', views.GrupCreate.as_view(), name='grup_create'),
    url(r'^grup/(?P<pk>\d+)/update/$', views.GrupUpdate.as_view(), name='grup_update'),
    url(r'^grup/(?P<pk>\d+)/delete/$', views.grup_sil, name='grup_sil'),
    url(r'^grup/(?P<pk>\d+)/delete/kesin/$', views.grup_sil_kesin, name='grup_sil_kesin'),


    # şirket urlleri aşağıda....
    url(r'^sirket/$', views.SirketListView.as_view(), name='sirket'),
    url(r'^sirket/(?P<pk>\d+)$', views.SirketDetailView.as_view(), name='sirket-detail'),
    url(r'^sirket/create/$', views.SirketCreate.as_view(), name='sirket_create'),
    url(r'^sirket/(?P<pk>\d+)/update/$', views.SirketUpdate.as_view(), name='sirket_update'),
    url(r'^sirket/(?P<pk>\d+)/delete/$', views.sirket_sil, name='sirket_sil'),
    url(r'^sirket/(?P<pk>\d+)/delete/kesin/$', views.sirket_sil_kesin, name='sirket_sil_kesin'),

    # proje urlleri aşağıda....
    url(r'^proje/$', views.ProjeListView.as_view(), name='proje'),
    url(r'^proje/(?P<pk>\d+)$', views.ProjeDetailView.as_view(), name='proje-detail'),
    url(r'^proje/create/$', views.ProjeCreate.as_view(), name='proje_create'),
    url(r'^proje/(?P<pk>\d+)/update/$', views.ProjeUpdate.as_view(), name='proje_update'),
    url(r'^proje/(?P<pk>\d+)/delete/$', views.proje_sil, name='proje_sil'),
    url(r'^proje/(?P<pk>\d+)/delete/kesin/$', views.proje_sil_kesin, name='proje_sil_kesin'),

#-------------------------------------------------------------------------------------------------

    # tip urlleri aşağıda....
    url(r'^tipi/$', views.TipiListView.as_view(), name='tipi'),
    url(r'^tipi/(?P<pk>\d+)$', views.TipiDetailView.as_view(), name='tipi-detail'),
    url(r'^tipi/create/$', views.TipiCreate.as_view(), name='tipi_create'),
    url(r'^tipi/(?P<pk>\d+)/update/$', views.TipiUpdate.as_view(), name='tipi_update'),
    url(r'^tipi/(?P<pk>\d+)/delete/$', views.tipi_sil, name='tipi_sil'),
    url(r'^tipi/(?P<pk>\d+)/delete/kesin/$', views.tipi_sil_kesin, name='tipi_sil_kesin'),

    # bolum urlleri aşağıda....
    url(r'^bolum/$', views.BolumListView.as_view(), name='bolum'),
    url(r'^bolum/(?P<pk>\d+)$', views.BolumDetailView.as_view(), name='bolum-detail'),
    url(r'^bolum/create/$', views.BolumCreate.as_view(), name='bolum_create'),
    url(r'^bolum/(?P<pk>\d+)/update/$', views.BolumUpdate.as_view(), name='bolum_update'),
    url(r'^bolum/(?P<pk>\d+)/delete/$', views.bolum_sil, name='bolum_sil'),
    url(r'^bolum/(?P<pk>\d+)/delete/kesin/$', views.sirket_sil_kesin, name='bolum_sil_kesin'),

    # detay urlleri aşağıda....
    url(r'^detay/$', views.DetayListView.as_view(), name='detay'),
    url(r'^detay/(?P<pk>\d+)$', views.DetayDetailView.as_view(), name='detay-detail'),
    url(r'^detay/create/$', views.DetayCreate.as_view(), name='detay_create'),
    url(r'^detay/(?P<pk>\d+)/update/$', views.DetayUpdate.as_view(), name='detay_update'),
    url(r'^detay/(?P<pk>\d+)/delete/$', views.detay_sil, name='detay_sil'),
    url(r'^detay/(?P<pk>\d+)/delete/kesin/$', views.detay_sil_kesin, name='detay_sil_kesin'),

#---------------------------------------------------------------------------------------------------
    # sonuç urlleri aşağıda....
    #url(r'^sonuc/$', views.SonucListView.as_view(), name='sonuc'),
    url(r'^sonuc/$', views.sonuc_denetim_sec, name='sonuc_denetim_sec'),
    url(r'^sonuc/(?P<pk>\d+)$', views.SonucDetailView.as_view(), name='sonuc-detail'),
    #url(r'^sonuc/(?P<pk>\d+)/update/$', views.SonucUpdate.as_view(), name='sonuc_update'),

#---------------------------------------------------------------------------------------------------
#   denetim urlleri .............................
    #url(r'^denetim/olustur/$', views.denetim_olustur, name='denetim_olustur'),
    url(r'^denetim/$', views.DenetimListView.as_view(), name='denetim'),
    url(r'^denetim/(?P<pk>\d+)$', views.DenetimDetailView.as_view(), name='denetim-detail'),
    url(r'^denetim/isemrisonrasi/$', views.isemrisonrasi_sec, name='isemrisonrasi_sec'),
    url(r'^denetim/isemrisonrasi/devam/$', views.isemrisonrasi_devam, name='isemrisonrasi_devam'),
    url(r'^denetim/isemrisonrasi/denetimiptal/$', views.denetim_iptal, name='denetim_iptal'),
    url(r'^denetim/isemrisonrasi/denetimiptal/devam/$', views.denetim_iptal_devam, name='denetim_iptal_devam'),
    url(r'^denetim/isemrisonrasi/denetcidegistir/$', views.denetci_degistir, name='denetci_degistir'),
    url(r'^denetim/isemrisonrasi/tarihdegistir/$', views.tarih_degistir, name='tarih_degistir'),
    #deneme alttaki.................
    url(r'^denetim/isemrisonrasi/deneme_filteredselectmultiple/$', views.deneme_filteredselectmultiple, name='deneme_filteredselectmultiple'),
    url(r'^denetim/baslanmislar/$', views.baslanmislar_sec, name='baslanmislar_sec'),
    url(r'^denetim/baslanmislar/devam/$', views.baslanmislar_devam, name='baslanmislar_devam'),
    url(r'^denetim/sonlandirilan/$', views.sonlandirilan_sec, name='sonlandirilan_sec'),
    url(r'^denetim/sonlandirilan/devam/$', views.sonlandirilan_devam, name='sonlandirilan_devam'),
    url(r'^denetim/sonlandirilan/devam/(?P<pk>\d+)$', views.sonlandirilan_ilerle, name='sonlandirilan_ilerle'),
    url(r'^denetim/create/$', views.denetim_create, name='denetim_create'),
    url(r'^denetim/(?P<pk>\d+)/update/$', views.DenetimUpdate.as_view(), name='denetim_update'),
    url(r'^denetim/(?P<pk>\d+)/delete/$', views.denetim_sil, name='denetim_sil'),
    url(r'^denetim/(?P<pk>\d+)/delete/kesin/$', views.denetim_sil_kesin, name='denetim_sil_kesin'),
#   diğer denetim oluşturma işlemleri..................
    url(r'^denetim/gozlemcisec/$', views.gozlemci_denetim_sec, name='gozlemci_denetim_sec'),
    url(r'^denetim/gozlemcisec/devam/$', views.gozlemci_sec_devam, name='gozlemci_sec_devam'),
    url(r'^denetim/bolumsec/$', views.bolum_denetim_sec, name='bolum_denetim_sec'),
    url(r'^denetim/bolumsec/devam/$', views.bolum_sec_devam, name='bolum_sec_devam'),
    url(r'^denetim/detaysec/$', views.detay_denetim_sec, name='detay_denetim_sec'),
    url(r'^denetim/detaysec/devam/$', views.detay_sec_devam, name='detay_sec_devam'),
    url(r'^denetim/detaysec/denetim_bolum_js/$', views.denetim_bolum_js, name='denetim_bolum_js'),
    url(r'^denetim/teksayfa_yarat/detaylarsec_bolum_js/$', views.detaylarsec_bolum_js, name='detaylarsec_bolum_js'),
    url(r'^denetim/isemriolustur/$', views.isemri_denetim_sec, name='isemri_denetim_sec'),
    url(r'^denetim/isemriolustur/devam/$', views.isemri_olustur_devam, name='isemri_olustur_devam'),
    url(r'^denetim/isemri/$', views.isemri_yarat, name='isemri_yarat'),
    url(r'^denetim/teksayfa_yarat/$', views.teksayfa_yarat, name='teksayfa_yarat'),

    #url(r'^denetim/goster/$', views.denetim_goster, name='denetim_goster'),

    ]
