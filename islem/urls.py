
from django.views.generic import RedirectView
from django.views.generic import View
#from django.conf.urls import include, url
from django.urls import re_path, path, include
from . import views
from django.utils.translation import gettext as _
from rest_framework import routers, serializers, viewsets
# from django.contrib.auth import views
#from django.conf.urls import include
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

from .views import denetimautocomplete, sonucbolumautocomplete, takipciautocomplete
from .views import bolumautocomplete, detayautocomplete, tipiautocomplete, spvautocomplete
from .views import zonautocomplete, denetciautocomplete, projeautocomplete, sirket2autocomplete
from .views import denolusturautocomplete, denetimrutinautocomplete, rutindenetimautocomplete
from .views import list_tipiautocomplete, list_zonautocomplete, list_bolumautocomplete
from .views import sirketautocomplete, sirketprojeautocomplete, spvautocomplete, denautocomplete
from notification.views import list_notification, show_notification, create_notification, delete_notification




urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    # dal denemesi için..................
    re_path(r'^denetim-autocomplete/$', denetimautocomplete.as_view(),name='denetim-autocomplete',),
    re_path(r'^denetim-rutin-autocomplete/$', denetimrutinautocomplete.as_view(),name='denetim-rutin-autocomplete',),
    re_path(r'^denolustur-autocomplete/$', denolusturautocomplete.as_view(),name='denolustur-autocomplete',),
    re_path(r'^sonucbolum-autocomplete/$', sonucbolumautocomplete.as_view(),name='sonucbolum-autocomplete',),
    re_path(r'^takipci-autocomplete/$', takipciautocomplete.as_view(),name='takipci-autocomplete',),
    re_path(r'^bolum-autocomplete/$', bolumautocomplete.as_view(),name='bolum-autocomplete',),
    re_path(r'^spv-autocomplete/$', spvautocomplete.as_view(),name='spv-autocomplete',),
    re_path(r'^den-autocomplete/$', denautocomplete.as_view(),name='den-autocomplete',),
    re_path(r'^detay-autocomplete/$', detayautocomplete.as_view(),name='detay-autocomplete',),
    re_path(r'^tipi-autocomplete/$', tipiautocomplete.as_view(),name='tipi-autocomplete',),
    re_path(r'^zon-autocomplete/$', zonautocomplete.as_view(),name='zon-autocomplete',),
    re_path(r'^proje-autocomplete/$', projeautocomplete.as_view(),name='proje-autocomplete',),
    re_path(r'^sirket2-autocomplete/$', sirket2autocomplete.as_view(),name='sirket2-autocomplete',),
    re_path(r'^denetci-autocomplete/$', denetciautocomplete.as_view(),name='denetci-autocomplete',),
    re_path(r'^rutindenetim-autocomplete/$', rutindenetimautocomplete.as_view(),name='rutindenetim-autocomplete',),
    re_path(r'^list_tipi-autocomplete/$', list_tipiautocomplete.as_view(),name='list_tipi-autocomplete',),
    re_path(r'^list_zon-autocomplete/$', list_zonautocomplete.as_view(),name='list_zon-autocomplete',),
    re_path(r'^list_bolum-autocomplete/$', list_bolumautocomplete.as_view(),name='list_bolum-autocomplete',),
    re_path(r'^sirket-autocomplete/$', sirketautocomplete.as_view(),name='sirket-autocomplete',),
    re_path(r'^sirketproje-autocomplete/$', sirketprojeautocomplete.as_view(),name='sirketproje-autocomplete',),


#  yerinde denetim ile ilgili işlemler...................
    re_path(r'^denetim/$', views.DenetimListView.as_view(), name='denetim'),
    re_path(r'^denetim/(?P<pk>\d+)$', views.denetim_detay, name='denetim_detay'),
    #re_path(r'^denetim/(?P<pk>\d+)/pdf/$', views.GeneratePDF.as_view(), name='GeneratePDF'),
    re_path(r'^denetim/(?P<pk>\d+)/pdf/$', views.generate_pdf, name='generate_pdf'),
    re_path(r'^baslat/$', views.denetim_baslat, name='denetim_baslat'),
    re_path(r'^baslat/kesin/$', views.denetim_baslat_kesin, name='denetim_baslat_kesin'),
    re_path(r'^devam/(?P<pk>\d+)$', views.denetim_devam_islemleri, name='denetim_devam_islemleri'),
    re_path(r'^tekrar/(?P<pk>\d+)$', views.denetim_tekrar_islemleri, name='denetim_tekrar_islemleri'),
    re_path(r'^tekrar/(?P<pk>\d+)/kesin/$', views.denetim_tekrarla_kesin, name='denetim_tekrarla_kesin'),
    re_path(r'^tamamla/(?P<pk>\d+)$', views.denetim_tamamla, name='denetim_tamamla'),
    re_path(r'^acilbildirim/(?P<pk>\d+)$', views.acil_bildirim, name='acil_bildirim'),
    re_path(r'^tamamla/(?P<pk>\d+)/kesin/$', views.denetim_tamamla_kesin, name='denetim_tamamla_kesin'),
    re_path(r'^devam_liste/$', views.devam_liste, name='devam_liste'),
    re_path(r'^rutin_baslat/$', views.rutin_baslat, name='rutin_baslat'),
    re_path(r'^rutin_baslat/kesin$', views.rutin_baslat_kesin, name='rutin_baslat_kesin'),
    re_path(r'^acil_devam_sec/$', views.acil_devam_sec, name='acil_devam_sec'),
    re_path(r'^qrcode/$', views.qrcode_tara, name='qrcode_tara'),
    re_path(r'^nfc_oku/(?P<pk>\d+)$', views.nfc_oku, name='nfc_oku'),
    re_path(r'^qrcode/result/$', views.qrcode_islemi_baslat, name='qrcode_islemi_baslat'),
    #re_path(r'^qrcode/(?P<pk>\d+)$', views.qrcode_calistir_js, name='qrcode_calistir_js'),
    re_path(r'^qrcode/qrcode_calistir_js/$', views.qrcode_calistir_js, name='qrcode_calistir_js'),

    re_path(r'^dosyalari_duzenle/$', views.dosyalari_duzenle, name='dosyalari_duzenle'),
    re_path(r'^dosyalari_duzenle/kesin$', views.dosyalari_duzenle_kesin, name='dosyalari_duzenle_kesin'),


    re_path(r'^bolum_sec/$', views.denetim_bolum_sec, name='denetim_bolum_sec'),
    re_path(r'^bolum_sec/secilen_bolumu_kaydet/$', views.secilen_bolumu_kaydet, name='secilen_bolumu_kaydet'),
    re_path(r'^bolum_sec/detay_islemleri_baslat/$', views.detay_islemleri_baslat, name='detay_islemleri_baslat'),
    re_path(r'^bolum_sec/denetim_detay_islemleri/$', views.denetim_detay_islemleri, name='denetim_detay_islemleri'),
    re_path(r'^bolum_sec/denetim_detay_islemleri/kucuk_resim_al/$', views.kucuk_resim_al, name='kucuk_resim_al'),
    re_path(r'^bolum_sec/denetim_detay_islemleri/kucuk_resim_sil/$', views.kucuk_resim_sil, name='kucuk_resim_sil'),
    re_path(r'^baslat/devam/denetim_detay_islemleri/kucuk_resim_al/$', views.kucuk_resim_al, name='kucuk_resim_al'),
    re_path(r'^baslat/devam/denetim_detay_islemleri/kucuk_resim_sil/$', views.kucuk_resim_sil, name='kucuk_resim_sil'),
    re_path(r'^baslat/devam/secilen_bolumu_kaydet/$', views.secilen_bolumu_kaydet, name='secilen_bolumu_kaydet'),
    re_path(r'^baslat/devam/detay_islemleri_baslat/$', views.detay_islemleri_baslat, name='detay_islemleri_baslat'),
    re_path(r'^baslat/devam/denetim_detay_islemleri/$', views.denetim_detay_islemleri, name='denetim_detay_islemleri'),


#---------------------------------------------------------------------------------------------------
    # sonuç re_pathleri aşağıda....
    #re_path(r'^sonuc/$', views.SonucListView.as_view(), name='sonuc'),
    re_path(r'^sonuc/$', views.sonuc_denetim_sec, name='sonuc_denetim_sec'),
    re_path(r'^sonuc/(?P<pk_den>\d+)/$', views.sonuc_denetim_sec_dogrudan, name='sonuc_denetim_sec_dogrudan'),
    #re_path(r'^sonuc/denetim_sec/(?P<pk>\d+)$', views.sonuc_denetim_sec_dogrudan, name='sonuc_denetim_sec_dogrudan'),
    re_path(r'^sonuc/(?P<pk_den>\d+)/(?P<pk>\d+)$', views.sonuc_denetim_detay_sec, name='sonuc_denetim_detay_sec'),
    re_path(r'^sonuc/(?P<pk>\d+)/(?P<pk_den>\d+)/duzenle/$', views.sonuc_denetim_detay_duzenle, name='sonuc_denetim_detay_duzenle'),
    re_path(r'^sonuc/(?P<pk>\d+)/(?P<pk_den>\d+)/duzenle/kucuk_resim_al/$', views.kucuk_resim_al, name='kucuk_resim_al'),
    re_path(r'^sonuc/(?P<pk>\d+)/(?P<pk_den>\d+)/duzenle/kucuk_resim_sil/$', views.kucuk_resim_sil, name='kucuk_resim_sil'),
    re_path(r'^sonuc/(?P<pk>\d+)/(?P<pk_den>\d+)/duzenle/update_resim_varmi/$', views.update_resim_varmi, name='update_resim_varmi'),
    re_path(r'^sonuc/(?P<pk>\d+)/(?P<pk_den>\d+)/duzenle/getvalue_resim_varmi/$', views.getvalue_resim_varmi, name='getvalue_resim_varmi'),
    #re_path(r'^sonuc/(?P<pk>\d+)$', views.SonucDetayDetailView.as_view(), name='sonuc-detail'),
    #re_path(r'^sonuc/(?P<pk>\d+)/update/$', views.SonucUpdate.as_view(), name='sonuc_update'),


#---------------------------------------------------------------------------------------------------
    # rest re_pathleri aşağıda....
    re_path(r'^memnuniyet_create/$', views.memnuniyet_create, name='memnuniyet_create'),
    re_path(r'^memnuniyet_list/$', views.memnuniyet_list, name='memnuniyet_list'),
    re_path(r'^operasyon_create/$', views.operasyon_create, name='operasyon_create'),
    re_path(r'^operasyon_list/$', views.operasyon_list, name='operasyon_list'),
    re_path(r'^den_saha_create/$', views.den_saha_create, name='den_saha_create'),
    re_path(r'^den_saha_list/$', views.den_saha_list, name='den_saha_list'),
    re_path(r'^ariza_create/$', views.ariza_create, name='ariza_create'),
    re_path(r'^ariza_list/$', views.ariza_list, name='ariza_list'),
    re_path(r'^sayi_create/$', views.sayi_create, name='sayi_create'),
    re_path(r'^sayi_list/$', views.sayi_list, name='sayi_list'),
    re_path(r'^rfid_create/$', views.rfid_create, name='rfid_create'),
    re_path(r'^rfid_list/$', views.rfid_list, name='rfid_list'),
    re_path(r'^rfid_filter/$', views.rfid_filter, name='rfid_filter'),
    re_path(r'^rfid_filter/(?P<proje>\d+)/$', views.rfid_filter_proje, name='rfid_filter_proje'),
    re_path(r'^macnoyer/$', views.macnoyer, name='macnoyer'),
    re_path(r'^macnoyer_degis/$', views.macnoyer_degis, name='macnoyer_degis'),
    re_path(r'^yerud_create/$', views.yerud_create, name='yerud_create'),
    re_path(r'^yerud_list/$', views.yerud_list, name='yerud_list'),
    re_path(r'^ad_yerud_list/$', views.ad_yerud_list, name='ad_yerud_list'),

    re_path(r'^deneme_dropdown/$', views.deneme_dropdown, name='deneme_dropdown'),



#---------------------------------------------------------------------------------------------------
#   denetim oluşturma re_path leri  eskiler .............................
    #
    re_path(r'^denetim/isemrisonrasi/$', views.isemrisonrasi_sec, name='isemrisonrasi_sec'),
    re_path(r'^denetim/isemrisonrasi/devam/$', views.isemrisonrasi_devam, name='isemrisonrasi_devam'),
    re_path(r'^denetim/isemrisonrasi/denetimiptal/$', views.denetim_iptal, name='denetim_iptal'),
    re_path(r'^denetim/isemrisonrasi/denetimiptal/devam/$', views.denetim_iptal_devam, name='denetim_iptal_devam'),
    re_path(r'^denetim/(?P<pk>\d+)/update/$', views.DenetimUpdate.as_view(), name='denetim_update'),

    #yeniler raporlama ve sonraki işlemler kısmı............
    re_path(r'^denetim/baslanmislar/$', views.baslanmislar_sec, name='baslanmislar_sec'),
    re_path(r'^denetim/baslanmislar/devam/$', views.baslanmislar_devam, name='baslanmislar_devam'),
    re_path(r'^denetim/sonlandirilan/$', views.sonlandirilan_sec, name='sonlandirilan_sec'),
    re_path(r'^denetim/sonlandirilan/devam/$', views.sonlandirilan_devam, name='sonlandirilan_devam'),
    re_path(r'^denetim/sonlandirilan/devam/(?P<pk>\d+)$', views.sonlandirilan_ilerle, name='sonlandirilan_ilerle'),
    re_path(r'^denetim/raporlar/$', views.raporlar_sec, name='raporlar_sec'),
    re_path(r'^denetim/raporlar/devam/$', views.raporlar_devam, name='raporlar_devam'),
    re_path(r'^denetim/raporlar/devam/(?P<pk>\d+)$', views.raporlar_ilerle, name='raporlar_ilerle'),
    re_path(r'^denetim/iptal/$', views.iptal_sec, name='iptal_sec'),
    re_path(r'^denetim/iptal/devam/$', views.iptal_devam, name='iptal_devam'),
    re_path(r'^denetim/iptal/devam/(?P<pk>\d+)$', views.iptal_ilerle, name='iptal_ilerle'),
    re_path(r'^rapor_yazisi/$', views.rapor_yazisi, name='rapor_yazisi'),
    re_path(r'^rapor_yazisi/rapor_yazisi_al/$', views.rapor_yazisi_al, name='rapor_yazisi_al'),

#   diğer denetim oluşturma işlemleri..................
    re_path(r'^denetim/teksayfa_yarat/$', views.teksayfa_yarat, name='teksayfa_yarat'),
    re_path(r'^denetim/teksayfa_yarat/detaylarsec_bolum_js/$', views.detaylarsec_bolum_js, name='detaylarsec_bolum_js'),
    re_path(r'^denetim/teksayfa_yarat/tipisec_bolum_js/$', views.tipisec_bolum_js, name='tipisec_bolum_js'),
    re_path(r'^denetim/teksayfa_duzenle/$', views.teksayfa_duzenle, name='teksayfa_duzenle'),
    re_path(r'^denetim/teksayfa_duzenle_devam/$', views.teksayfa_duzenle_devam, name='teksayfa_duzenle_devam'),
    re_path(r'^denetim/teksayfa_duzenle_devam/detaylarsec_bolum_js_2/$', views.detaylarsec_bolum_js_2, name='detaylarsec_bolum_js_2'),
    re_path(r'^denetim/teksayfa_duzenle_devam/tipisec_bolum_js_2/$', views.tipisec_bolum_js_2, name='tipisec_bolum_js_2'),
    re_path(r'^denetim/teksayfa_sil/$', views.teksayfa_sil, name='teksayfa_sil'),
    re_path(r'^denetim/teksayfa_sil_kesin/$', views.teksayfa_sil_kesin, name='teksayfa_sil_kesin'),

#---------------------------------------------------------------------------------------------

#   kullanıcı ile ilgili işlemler..................
    re_path(r'^kullanici_ekle/$', views.kullanici_ekle, name='kullanici_ekle'),
    #re_path(r'^kullanici_duzenle/$', views.kullanici_duzenle, name='kullanici_duzenle'),
    #re_path(r'^kullanici_kaldir/$', views.kullanici_kaldir, name='kullanici_kaldir'),
    #re_path(r'^kullanici_aktif/$', views.kullanici_aktif, name='kullanici_aktif'),
    #re_path(r'^kullanici_resim/$', views.kullanici_resim, name='kullanici_resim'),
    #re_path(r'^kullanici_sifre/$', views.kullanici_sifre, name='kullanici_sifre'),
    #re_path(r'^ipy_ata/$', views.ipy_ata, name='ipy_ata'),

#-------------------------------------------------------------------------------------------------
    # grup re_pathleri aşağıda....
    re_path(r'^deneme/$', views.deneme_denetim, name='deneme_denetim'),
    re_path(r'^deneme_iki/$', views.deneme_sonucbolum, name='deneme_sonucbolum'),
    re_path(r'^deneme_uc/$', views.deneme_nebu, name='deneme_nebu'),


    re_path(r'^grup/$', views.GrupListView.as_view(), name='grup'),
    re_path(r'^grup/(?P<pk>\d+)$', views.GrupDetailView.as_view(), name='grup-detail'),
    re_path(r'^grup/create/$', views.GrupCreate.as_view(), name='grup_create'),
    re_path(r'^grup/(?P<pk>\d+)/update/$', views.GrupUpdate.as_view(), name='grup_update'),
    re_path(r'^grup/(?P<pk>\d+)/delete/$', views.grup_sil, name='grup_sil'),
    re_path(r'^grup/(?P<pk>\d+)/delete/kesin/$', views.grup_sil_kesin, name='grup_sil_kesin'),


    # şirket re_pathleri aşağıda....
    re_path(r'^sirket/$', views.SirketListView.as_view(), name='sirket'),
    re_path(r'^sirket/(?P<pk>\d+)$', views.SirketDetailView.as_view(), name='sirket-detail'),
    re_path(r'^sirket/create/$', views.SirketCreate.as_view(), name='sirket_create'),
    re_path(r'^sirket/(?P<pk>\d+)/update/$', views.SirketUpdate.as_view(), name='sirket_update'),
    re_path(r'^sirket/(?P<pk>\d+)/delete/$', views.sirket_sil, name='sirket_sil'),
    re_path(r'^sirket/(?P<pk>\d+)/delete/kesin/$', views.sirket_sil_kesin, name='sirket_sil_kesin'),

    # proje re_pathleri aşağıda....
    re_path(r'^proje/$', views.ProjeListView.as_view(), name='proje'),
    re_path(r'^proje/(?P<pk>\d+)$', views.ProjeDetailView.as_view(), name='proje-detail'),
    re_path(r'^proje/create/$', views.ProjeCreate.as_view(), name='proje_create'),
    re_path(r'^proje/(?P<pk>\d+)/update/$', views.ProjeUpdate.as_view(), name='proje_update'),
    re_path(r'^proje/(?P<pk>\d+)/delete/$', views.proje_sil, name='proje_sil'),
    re_path(r'^proje/(?P<pk>\d+)/delete/kesin/$', views.proje_sil_kesin, name='proje_sil_kesin'),

#-------------------------------------------------------------------------------------------------

    # tip re_pathleri aşağıda....
    re_path(r'^tipi/$', views.TipiListView.as_view(), name='tipi'),
    re_path(r'^tipi/(?P<pk>\d+)$', views.TipiDetailView.as_view(), name='tipi-detail'),
    re_path(r'^tipi/create/$', views.TipiCreate.as_view(), name='tipi_create'),
    re_path(r'^tipi/(?P<pk>\d+)/update/$', views.TipiUpdate.as_view(), name='tipi_update'),
    re_path(r'^tipi/(?P<pk>\d+)/delete/$', views.tipi_sil, name='tipi_sil'),
    re_path(r'^tipi/(?P<pk>\d+)/delete/kesin/$', views.tipi_sil_kesin, name='tipi_sil_kesin'),

    # zon re_pathleri aşağıda....
    re_path(r'^zon/$', views.ZonListView.as_view(), name='zon'),
    re_path(r'^zon/(?P<pk>\d+)$', views.ZonDetailView.as_view(), name='zon-detail'),
    re_path(r'^zon/create/$', views.ZonCreate.as_view(), name='zon_create'),
    re_path(r'^zon/(?P<pk>\d+)/update/$', views.ZonUpdate.as_view(), name='zon_update'),
    re_path(r'^zon/(?P<pk>\d+)/delete/$', views.zon_sil, name='zon_sil'),
    re_path(r'^zon/(?P<pk>\d+)/delete/kesin/$', views.zon_sil_kesin, name='zon_sil_kesin'),


    # bolum re_pathleri aşağıda....
    re_path(r'^bolum/$', views.BolumListView.as_view(), name='bolum'),
    re_path(r'^bolum/(?P<pk>\d+)$', views.BolumDetailView.as_view(), name='bolum-detail'),
    re_path(r'^bolum/create/$', views.BolumCreate.as_view(), name='bolum_create'),
    re_path(r'^bolum/(?P<pk>\d+)/update/$', views.BolumUpdate.as_view(), name='bolum_update'),
    re_path(r'^bolum/(?P<pk>\d+)/delete/$', views.bolum_sil, name='bolum_sil'),
    re_path(r'^bolum/(?P<pk>\d+)/delete/kesin/$', views.sirket_sil_kesin, name='bolum_sil_kesin'),

    re_path(r'^soru_listesi/$', views.soru_listesi, name='soru_listesi'),
    re_path(r'^soru_listesi/devam/$', views.soru_listesi_devam, name='soru_listesi_devam'),
    re_path(r'^soru_listesi/devam/yarat/$', views.soru_listesi_yarat, name='soru_listesi_yarat'),
    re_path(r'^soru_listesi/devam/(?P<pk>\d+)/duzenle/$', views.soru_listesi_duzenle, name='soru_listesi_duzenle'),
    re_path(r'^soru_listesi/devam/(?P<pk>\d+)/sil/$', views.soru_listesi_sil, name='soru_listesi_sil'),
    re_path(r'^soru_listesi/devam/(?P<pk>\d+)/sil/kesin/$', views.soru_listesi_sil_kesin, name='soru_listesi_sil_kesin'),
    re_path(r'^soru_listesi/devam/kopyala/$', views.soru_listesi_kopyala, name='soru_listesi_kopyala'),
    re_path(r'^soru_listesi/devam/kopyala/kopyala_js/$', views.soru_kopyala_js, name='soru_kopyala_js'),
    re_path(r'^soru_listesi/devam/kopyala/kesin$', views.soru_listesi_kopyala_kesin, name='soru_listesi_kopyala_kesin'),

    re_path(r'^bolum_listesi/$', views.bolum_listesi, name='bolum_listesi'),
    re_path(r'^bolum_listesi/devam/$', views.bolum_listesi_devam, name='bolum_listesi_devam'),
    re_path(r'^bolum_listesi/devam/yarat/$', views.bolum_listesi_yarat, name='bolum_listesi_yarat'),
    re_path(r'^bolum_listesi/devam/(?P<pk>\d+)/duzenle/$', views.bolum_listesi_duzenle, name='bolum_listesi_duzenle'),
    re_path(r'^bolum_listesi/devam/(?P<pk>\d+)/sil/$', views.bolum_listesi_sil, name='bolum_listesi_sil'),
    re_path(r'^bolum_listesi/devam/(?P<pk>\d+)/sil/kesin/$', views.bolum_listesi_sil_kesin, name='bolum_listesi_sil_kesin'),

    re_path(r'^zon_listesi/$', views.zon_listesi, name='zon_listesi'),
    re_path(r'^zon_listesi/devam/$', views.zon_listesi_devam, name='zon_listesi_devam'),
    re_path(r'^zon_listesi/devam/yarat/$', views.zon_listesi_yarat, name='zon_listesi_yarat'),
    re_path(r'^zon_listesi/devam/(?P<pk>\d+)/duzenle/$', views.zon_listesi_duzenle, name='zon_listesi_duzenle'),
    re_path(r'^zon_listesi/devam/(?P<pk>\d+)/sil/$', views.zon_listesi_sil, name='zon_listesi_sil'),
    re_path(r'^zon_listesi/devam/(?P<pk>\d+)/sil/kesin/$', views.zon_listesi_sil_kesin, name='zon_listesi_sil_kesin'),

    re_path(r'^spv_listesi/$', views.spv_listesi, name='spv_listesi'),
    re_path(r'^spv_listesi/yarat/$', views.spv_yarat, name='spv_yarat'),
    re_path(r'^spv_listesi/(?P<pk>\d+)/sil/$', views.spv_listesi_sil, name='spv_listesi_sil'),
    re_path(r'^spv_listesi/(?P<pk>\d+)/sil/kesin/$', views.spv_listesi_sil_kesin, name='spv_listesi_sil_kesin'),

    re_path(r'^den_listesi/$', views.den_listesi, name='den_listesi'),
    re_path(r'^den_listesi/yarat/$', views.den_yarat, name='den_yarat'),
    re_path(r'^den_listesi/(?P<pk>\d+)/sil/$', views.den_listesi_sil, name='den_listesi_sil'),
    re_path(r'^den_listesi/(?P<pk>\d+)/sil/kesin/$', views.den_listesi_sil_kesin, name='den_listesi_sil_kesin'),

    re_path(r'^opr_admin/$', views.opr_admin, name='opr_admin'),
    re_path(r'^opr_admin/(?P<pk>\d+)/ekle/$', views.opr_admin_ekle, name='opr_admin_ekle'),
    re_path(r'^opr_admin/(?P<pk>\d+)/ekle/kesin/$', views.opr_admin_ekle_kesin, name='opr_admin_ekle_kesin'),
    re_path(r'^opr_admin/(?P<pk>\d+)/kaldir/$', views.opr_admin_kaldir, name='opr_admin_kaldir'),
    re_path(r'^opr_admin/(?P<pk>\d+)/kaldir/kesin/$', views.opr_admin_kaldir_kesin, name='opr_admin_kaldir_kesin'),

    # detay re_pathleri aşağıda....
    re_path(r'^detay/$', views.DetayListView.as_view(), name='detay'),
    re_path(r'^detay/(?P<pk>\d+)$', views.DetayDetailView.as_view(), name='detay-detail'),
    re_path(r'^detay/create/$', views.DetayCreate.as_view(), name='detay_create'),
    re_path(r'^detay/(?P<pk>\d+)/update/$', views.DetayUpdate.as_view(), name='detay_update'),
    re_path(r'^detay/(?P<pk>\d+)/delete/$', views.detay_sil, name='detay_sil'),
    re_path(r'^detay/(?P<pk>\d+)/delete/kesin/$', views.detay_sil_kesin, name='detay_sil_kesin'),

    # projealanlari re_pathleri aşağıda....
    #re_path(r'^projealanlari/$', views.ProjeAlanlariListView.as_view(), name='projealanlari'),
    re_path(r'^projealanlari/$', views.projealanlari_listele, name='projealanlari_listele'),
    re_path(r'^projealanlari/(?P<pk>\d+)$', views.ProjeAlanlariDetailView.as_view(), name='projealanlari-detail'),
    #re_path(r'^projealanlari/create/$', views.ProjeAlanlariCreate.as_view(), name='projealanlari_create'),
    re_path(r'^projealanlari/create/$', views.projealanlari_yarat, name='projealanlari_yarat'),
    re_path(r'^projealanlari/(?P<pk>\d+)/update/$', views.ProjeAlanlariUpdate.as_view(), name='projealanlari_update'),
    re_path(r'^projealanlari/(?P<pk>\d+)/delete/$', views.projealanlari_sil, name='projealanlari_sil'),
    re_path(r'^projealanlari/(?P<pk>\d+)/delete/kesin/$', views.projealanlari_sil_kesin, name='projealanlari_sil_kesin'),

    # rfid dosyası - ws olmayan -  re_pathleri aşağıda....
    re_path(r'^rfid/$', views.rfid_dosyasi_listele, name='rfid_dosyasi_listele'),
    re_path(r'^rfid/(?P<pk>\d+)$', views.rfid_dosyasi_detay, name='rfid_dosyasi_detay'),
    re_path(r'^rfid/create/$', views.rfid_dosyasi_yarat, name='rfid_dosyasi_yarat'),
    re_path(r'^rfid/(?P<pk>\d+)/update/$', views.rfid_dosyasi_duzenle, name='rfid_dosyasi_duzenle'),
    re_path(r'^rfid/(?P<pk>\d+)/delete/$', views.rfid_dosyasi_sil, name='rfid_dosyasi_sil'),
    re_path(r'^rfid/(?P<pk>\d+)/delete/kesin/$', views.rfid_dosyasi_sil_kesin, name='rfid_dosyasi_sil_kesin'),

    #proje elemanlarının tanımlanmasına yönelik re_path ler aşağıda...
    re_path(r'^eleman/$', views.eleman_listele, name='eleman_listele'),
    re_path(r'^eleman/(?P<pk>\d+)$', views.eleman_detay, name='eleman_detay'),
    re_path(r'^eleman/create/$', views.eleman_yarat, name='eleman_yarat'),
    re_path(r'^eleman/(?P<pk>\d+)/update/$', views.eleman_duzenle, name='eleman_duzenle'),
    re_path(r'^eskibul/$', views.eleman_eskibul, name='eleman_eskibul'),
    #re_path(r'^eleman/eskibul/(?P<pk>\d+)$', views.eleman_eskibul_detay, name='eleman_eskibul_detay'),
    re_path(r'^eskibul/(?P<pk>\d+)/kesin/$', views.eleman_eskibul_kesin, name='eleman_eskibul_kesin'),


    # yer re_pathleri aşağıda....
    re_path(r'^yer/$', views.yer_listele, name='yer_listele'),
    re_path(r'^yer/(?P<pk>\d+)/$', views.yer_detay, name='yer_detay'),
    re_path(r'^yer/(?P<pk>\d+)/yer_operasyon_ekle/$', views.yer_operasyon_ekle, name='yer_operasyon_ekle'),
    re_path(r'^yer/(?P<pk>\d+)/yer_operasyon_planla/$', views.yer_operasyon_planla, name='yer_operasyon_planla'),
    re_path(r'^yer/(?P<pk>\d+)/(?P<pk2>\d+)/update/$', views.yer_operasyon_duzenle, name='yer_operasyon_duzenle'),
    re_path(r'^yer/(?P<pk>\d+)/(?P<pk2>\d+)/delete/$', views.yer_operasyon_sil, name='yer_operasyon_sil'),
    re_path(r'^yer/(?P<pk>\d+)/(?P<pk2>\d+)/delete/kesin/$', views.yer_operasyon_sil_kesin, name='yer_operasyon_sil_kesin'),
    re_path(r'^yer/(?P<pk>\d+)/yer_denetim_ekle/$', views.yer_denetim_ekle, name='yer_denetim_ekle'),
    re_path(r'^yer/(?P<pk>\d+)/yer_denetim_planla/$', views.yer_denetim_planla, name='yer_denetim_planla'),
    re_path(r'^yer/(?P<pk>\d+)/(?P<pk2>\d+)/den/update/$', views.yer_denetim_duzenle, name='yer_denetim_duzenle'),
    re_path(r'^yer/(?P<pk>\d+)/(?P<pk2>\d+)/den/delete/$', views.yer_denetim_sil, name='yer_denetim_sil'),
    re_path(r'^yer/(?P<pk>\d+)/(?P<pk2>\d+)/den/delete/kesin/$', views.yer_denetim_sil_kesin, name='yer_denetim_sil_kesin'),

    re_path(r'^yer/create/$', views.yer_yarat, name='yer_yarat'),
    re_path(r'^yer/(?P<pk>\d+)/update/$', views.yer_duzenle, name='yer_duzenle'),
    re_path(r'^yer/(?P<pk>\d+)/delete/$', views.yer_sil, name='yer_sil'),
    re_path(r'^yer/(?P<pk>\d+)/delete/kesin/$', views.yer_sil_kesin, name='yer_sil_kesin'),


    # mk için olan re_path ler
    re_path(r'^mk_projealanlari/$', views.mk_projealanlari_listele, name='mk_projealanlari_listele'),
    re_path(r'^mk_yer/$', views.mk_yer_listele, name='mk_yer_proje_listele'),
    re_path(r'^mk_rfid/$', views.mk_rfid_listele, name='mk_rfid_proje_listele'),
    re_path(r'^mk_memnuniyet_list/$', views.mk_memnuniyet_list, name='mk_memnuniyet_list'),
    re_path(r'^mk_operasyon_list/$', views.mk_operasyon_list, name='mk_operasyon_list'),
    re_path(r'^mk_den_saha_list/$', views.mk_den_saha_list, name='mk_den_saha_list'),
    re_path(r'^mk_ariza_list/$', views.mk_ariza_list, name='mk_ariza_list'),
    re_path(r'^mk_sayi_list/$', views.mk_sayi_list, name='mk_sayi_list'),


    re_path(r'^rapormemnuniyet/$', views.rapor_memnuniyet, name='rapor_memnuniyet'),
    re_path(r'^rapor_mk_memnuniyet/$', views.rapor_mk_memnuniyet, name='rapor_mk_memnuniyet'),
    re_path(r'^rapor_krs_memnuniyet/$', views.rapor_krs_memnuniyet, name='rapor_krs_memnuniyet'),
    re_path(r'^gunlukyer/$', views.gunluk_yer, name='gunluk_yer'),

    # qrcode re_pathleri aşağıda....""
    re_path(r'^qrdosyasi/$', views.QrdosyasiListView.as_view(), name='qrdosyasi'),
    re_path(r'^qrdosyasi/(?P<pk>\d+)$', views.QrdosyasiDetailView.as_view(), name='qrdosyasi-detail'),
    re_path(r'^qrdosyasi/create/$', views.qrdosyasi_create, name='qrdosyasi_create'),
    re_path(r'^qrdosyasi/(?P<pk>\d+)/update/$', views.qrdosyasi_update, name='qrdosyasi_update'),
    re_path(r'^qrdosyasi/(?P<pk>\d+)/delete/$', views.qrdosyasi_sil, name='qrdosyasi_sil'),
    re_path(r'^qrdosyasi/(?P<pk>\d+)/delete/kesin/$', views.qrdosyasi_sil_kesin, name='qrdosyasi_sil_kesin'),

    re_path(r'^cagir1/$', views.cagir1, name='cagir1'),
    re_path(r'^cagir2/$', views.cagir2, name='cagir2'),
    re_path(r'^cagir3/$', views.cagir3, name='cagir3'),
    re_path(r'^cagir4/$', views.cagir4, name='cagir4'),

    re_path(r'^notification/$', views.list_notification, name='list_notification'),
    re_path(r'^notification/show/(?P<notification_id>\d+)/$', views.show_notification, name='show_notification'),
    re_path(r'^notification/delete/(?P<notification_id>\d+)/(?P<page_id>\d+)/$', views.delete_notification, name='delete_notification'),
    re_path(r'^notification/create/$', views.create_notification, name='create_notification'),

    re_path(r'^sms_mesaj/$', views.sms_mesaj, name='sms_mesaj'),

    ]
