
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

from .views import denetimautocomplete, sonucbolumautocomplete, takipciautocomplete
from .views import bolumautocomplete, detayautocomplete, tipiautocomplete
from .views import zonautocomplete, denetciautocomplete, projeautocomplete
from .views import denolusturautocomplete, denetimrutinautocomplete, rutindenetimautocomplete
from .views import list_tipiautocomplete, list_zonautocomplete, list_bolumautocomplete
from notification.views import list_notification, show_notification, create_notification, delete_notification




urlpatterns = [
    url(r'^$', views.index, name='index'),
    # dal denemesi için..................
    url(r'^denetim-autocomplete/$', denetimautocomplete.as_view(),name='denetim-autocomplete',),
    url(r'^denetim-rutin-autocomplete/$', denetimrutinautocomplete.as_view(),name='denetim-rutin-autocomplete',),
    url(r'^denolustur-autocomplete/$', denolusturautocomplete.as_view(),name='denolustur-autocomplete',),
    url(r'^sonucbolum-autocomplete/$', sonucbolumautocomplete.as_view(),name='sonucbolum-autocomplete',),
    url(r'^takipci-autocomplete/$', takipciautocomplete.as_view(),name='takipci-autocomplete',),
    url(r'^bolum-autocomplete/$', bolumautocomplete.as_view(),name='bolum-autocomplete',),
    url(r'^detay-autocomplete/$', detayautocomplete.as_view(),name='detay-autocomplete',),
    url(r'^tipi-autocomplete/$', tipiautocomplete.as_view(),name='tipi-autocomplete',),
    url(r'^zon-autocomplete/$', zonautocomplete.as_view(),name='zon-autocomplete',),
    url(r'^proje-autocomplete/$', projeautocomplete.as_view(),name='proje-autocomplete',),
    url(r'^denetci-autocomplete/$', denetciautocomplete.as_view(),name='denetci-autocomplete',),
    url(r'^rutindenetim-autocomplete/$', rutindenetimautocomplete.as_view(),name='rutindenetim-autocomplete',),
    url(r'^list_tipi-autocomplete/$', list_tipiautocomplete.as_view(),name='list_tipi-autocomplete',),
    url(r'^list_zon-autocomplete/$', list_zonautocomplete.as_view(),name='list_zon-autocomplete',),
    url(r'^list_bolum-autocomplete/$', list_bolumautocomplete.as_view(),name='list_bolum-autocomplete',),



#  yerinde denetim ile ilgili işlemler...................
    url(r'^denetim/$', views.DenetimListView.as_view(), name='denetim'),
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
    url(r'^rutin_baslat/$', views.rutin_baslat, name='rutin_baslat'),
    url(r'^rutin_baslat/kesin$', views.rutin_baslat_kesin, name='rutin_baslat_kesin'),
    url(r'^acil_devam_sec/$', views.acil_devam_sec, name='acil_devam_sec'),
    url(r'^qrcode/$', views.qrcode_tara, name='qrcode_tara'),
    url(r'^nfc_oku/(?P<pk>\d+)$', views.nfc_oku, name='nfc_oku'),
    url(r'^qrcode/result/$', views.qrcode_islemi_baslat, name='qrcode_islemi_baslat'),
    #url(r'^qrcode/(?P<pk>\d+)$', views.qrcode_calistir_js, name='qrcode_calistir_js'),
    url(r'^qrcode/qrcode_calistir_js/$', views.qrcode_calistir_js, name='qrcode_calistir_js'),
    url(r'^bolum_sec/$', views.denetim_bolum_sec, name='denetim_bolum_sec'),
    url(r'^bolum_sec/secilen_bolumu_kaydet/$', views.secilen_bolumu_kaydet, name='secilen_bolumu_kaydet'),
    url(r'^bolum_sec/detay_islemleri_baslat/$', views.detay_islemleri_baslat, name='detay_islemleri_baslat'),
    url(r'^bolum_sec/denetim_detay_islemleri/$', views.denetim_detay_islemleri, name='denetim_detay_islemleri'),
    #url(r'^bolum_sec/denetim_detay_islemleri/kucuk_resim_al/$', views.kucuk_resim_al, name='kucuk_resim_al'),
    url(r'^baslat/devam/denetim_detay_islemleri/kucuk_resim_al/$', views.kucuk_resim_al, name='kucuk_resim_al'),
    url(r'^baslat/devam/secilen_bolumu_kaydet/$', views.secilen_bolumu_kaydet, name='secilen_bolumu_kaydet'),
    url(r'^baslat/devam/detay_islemleri_baslat/$', views.detay_islemleri_baslat, name='detay_islemleri_baslat'),
    url(r'^baslat/devam/denetim_detay_islemleri/$', views.denetim_detay_islemleri, name='denetim_detay_islemleri'),


#---------------------------------------------------------------------------------------------------
    # sonuç urlleri aşağıda....
    #url(r'^sonuc/$', views.SonucListView.as_view(), name='sonuc'),
    url(r'^sonuc/$', views.sonuc_denetim_sec, name='sonuc_denetim_sec'),
    url(r'^sonuc/(?P<pk>\d+)$', views.sonuc_denetim_detay_sec, name='sonuc_denetim_detay_sec'),
    url(r'^sonuc/(?P<pk>\d+)/duzenle/$', views.sonuc_denetim_detay_duzenle, name='sonuc_denetim_detay_duzenle'),
    url(r'^sonuc/(?P<pk>\d+)/duzenle/kucuk_resim_al/$', views.kucuk_resim_al, name='kucuk_resim_al_2'),
    url(r'^sonuc/(?P<pk>\d+)/duzenle/update_resim_varmi/$', views.update_resim_varmi, name='update_resim_varmi'),
    url(r'^sonuc/(?P<pk>\d+)/duzenle/getvalue_resim_varmi/$', views.getvalue_resim_varmi, name='getvalue_resim_varmi'),
    #url(r'^sonuc/(?P<pk>\d+)$', views.SonucDetayDetailView.as_view(), name='sonuc-detail'),
    #url(r'^sonuc/(?P<pk>\d+)/update/$', views.SonucUpdate.as_view(), name='sonuc_update'),


#---------------------------------------------------------------------------------------------------
    # rest urlleri aşağıda....
    url(r'^memnuniyet_create/$', views.memnuniyet_create, name='memnuniyet_create'),
    url(r'^memnuniyet_list/$', views.memnuniyet_list, name='memnuniyet_list'),
    url(r'^operasyon_create/$', views.operasyon_create, name='operasyon_create'),
    url(r'^operasyon_list/$', views.operasyon_list, name='operasyon_list'),
    url(r'^den_saha_create/$', views.den_saha_create, name='den_saha_create'),
    url(r'^den_saha_list/$', views.den_saha_list, name='den_saha_list'),
    url(r'^ariza_create/$', views.ariza_create, name='ariza_create'),
    url(r'^ariza_list/$', views.ariza_list, name='ariza_list'),
    url(r'^rfid_create/$', views.rfid_create, name='rfid_create'),
    url(r'^rfid_list/$', views.rfid_list, name='rfid_list'),
    url(r'^rfid_filter/$', views.rfid_filter, name='rfid_filter'),
    url(r'^rfid_filter/(?P<proje>\d+)/$', views.rfid_filter_proje, name='rfid_filter_proje'),
    url(r'^macnoyer/$', views.macnoyer, name='macnoyer'),
    url(r'^macnoyer_degis/$', views.macnoyer_degis, name='macnoyer_degis'),
    url(r'^yerud_create/$', views.yerud_create, name='yerud_create'),
    url(r'^yerud_list/$', views.yerud_list, name='yerud_list'),


    url(r'^deneme_dropdown/$', views.deneme_dropdown, name='deneme_dropdown'),



#---------------------------------------------------------------------------------------------------
#   denetim oluşturma url leri  eskiler .............................
    #
    url(r'^denetim/isemrisonrasi/$', views.isemrisonrasi_sec, name='isemrisonrasi_sec'),
    url(r'^denetim/isemrisonrasi/devam/$', views.isemrisonrasi_devam, name='isemrisonrasi_devam'),
    url(r'^denetim/isemrisonrasi/denetimiptal/$', views.denetim_iptal, name='denetim_iptal'),
    url(r'^denetim/isemrisonrasi/denetimiptal/devam/$', views.denetim_iptal_devam, name='denetim_iptal_devam'),
    url(r'^denetim/(?P<pk>\d+)/update/$', views.DenetimUpdate.as_view(), name='denetim_update'),

    #yeniler raporlama ve sonraki işlemler kısmı............
    url(r'^denetim/baslanmislar/$', views.baslanmislar_sec, name='baslanmislar_sec'),
    url(r'^denetim/baslanmislar/devam/$', views.baslanmislar_devam, name='baslanmislar_devam'),
    url(r'^denetim/sonlandirilan/$', views.sonlandirilan_sec, name='sonlandirilan_sec'),
    url(r'^denetim/sonlandirilan/devam/$', views.sonlandirilan_devam, name='sonlandirilan_devam'),
    url(r'^denetim/sonlandirilan/devam/(?P<pk>\d+)$', views.sonlandirilan_ilerle, name='sonlandirilan_ilerle'),
    url(r'^denetim/raporlar/$', views.raporlar_sec, name='raporlar_sec'),
    url(r'^denetim/raporlar/devam/$', views.raporlar_devam, name='raporlar_devam'),
    url(r'^denetim/raporlar/devam/(?P<pk>\d+)$', views.raporlar_ilerle, name='raporlar_ilerle'),
    url(r'^denetim/iptal/$', views.iptal_sec, name='iptal_sec'),
    url(r'^denetim/iptal/devam/$', views.iptal_devam, name='iptal_devam'),
    url(r'^denetim/iptal/devam/(?P<pk>\d+)$', views.iptal_ilerle, name='iptal_ilerle'),
    url(r'^rapor_yazisi/$', views.rapor_yazisi, name='rapor_yazisi'),
    url(r'^rapor_yazisi/rapor_yazisi_al/$', views.rapor_yazisi_al, name='rapor_yazisi_al'),

#   diğer denetim oluşturma işlemleri..................
    url(r'^denetim/teksayfa_yarat/$', views.teksayfa_yarat, name='teksayfa_yarat'),
    url(r'^denetim/teksayfa_yarat/detaylarsec_bolum_js/$', views.detaylarsec_bolum_js, name='detaylarsec_bolum_js'),
    url(r'^denetim/teksayfa_yarat/tipisec_bolum_js/$', views.tipisec_bolum_js, name='tipisec_bolum_js'),
    url(r'^denetim/teksayfa_duzenle/$', views.teksayfa_duzenle, name='teksayfa_duzenle'),
    url(r'^denetim/teksayfa_duzenle_devam/$', views.teksayfa_duzenle_devam, name='teksayfa_duzenle_devam'),
    url(r'^denetim/teksayfa_duzenle_devam/detaylarsec_bolum_js_2/$', views.detaylarsec_bolum_js_2, name='detaylarsec_bolum_js_2'),
    url(r'^denetim/teksayfa_duzenle_devam/tipisec_bolum_js_2/$', views.tipisec_bolum_js_2, name='tipisec_bolum_js_2'),
    url(r'^denetim/teksayfa_sil/$', views.teksayfa_sil, name='teksayfa_sil'),
    url(r'^denetim/teksayfa_sil_kesin/$', views.teksayfa_sil_kesin, name='teksayfa_sil_kesin'),



#-------------------------------------------------------------------------------------------------
    # grup urlleri aşağıda....
    url(r'^deneme/$', views.deneme_denetim, name='deneme_denetim'),
    url(r'^deneme_iki/$', views.deneme_sonucbolum, name='deneme_sonucbolum'),
    url(r'^deneme_uc/$', views.deneme_nebu, name='deneme_nebu'),



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

    # zon urlleri aşağıda....
    url(r'^zon/$', views.ZonListView.as_view(), name='zon'),
    url(r'^zon/(?P<pk>\d+)$', views.ZonDetailView.as_view(), name='zon-detail'),
    url(r'^zon/create/$', views.ZonCreate.as_view(), name='zon_create'),
    url(r'^zon/(?P<pk>\d+)/update/$', views.ZonUpdate.as_view(), name='zon_update'),
    url(r'^zon/(?P<pk>\d+)/delete/$', views.zon_sil, name='zon_sil'),
    url(r'^zon/(?P<pk>\d+)/delete/kesin/$', views.zon_sil_kesin, name='zon_sil_kesin'),


    # bolum urlleri aşağıda....
    url(r'^bolum/$', views.BolumListView.as_view(), name='bolum'),
    url(r'^soru_listesi/$', views.soru_listesi, name='soru_listesi'),
    url(r'^soru_listesi/devam/$', views.soru_listesi_devam, name='soru_listesi_devam'),
    url(r'^soru_listesi/devam/yarat/$', views.soru_listesi_yarat, name='soru_listesi_yarat'),
    url(r'^soru_listesi/devam/(?P<pk>\d+)/duzenle/$', views.soru_listesi_duzenle, name='soru_listesi_duzenle'),
    url(r'^soru_listesi/devam/(?P<pk>\d+)/sil/$', views.soru_listesi_sil, name='soru_listesi_sil'),
    url(r'^soru_listesi/devam/(?P<pk>\d+)/sil/kesin/$', views.soru_listesi_sil_kesin, name='soru_listesi_sil_kesin'),
    url(r'^soru_listesi/devam/kopyala/$', views.soru_listesi_kopyala, name='soru_listesi_kopyala'),
    url(r'^soru_listesi/devam/kopyala/kopyala_js/$', views.soru_kopyala_js, name='soru_kopyala_js'),
    url(r'^soru_listesi/devam/kopyala/kesin$', views.soru_listesi_kopyala_kesin, name='soru_listesi_kopyala_kesin'),
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

    # projealanlari urlleri aşağıda....
    #url(r'^projealanlari/$', views.ProjeAlanlariListView.as_view(), name='projealanlari'),
    url(r'^projealanlari/$', views.projealanlari_listele, name='projealanlari_listele'),
    url(r'^projealanlari/(?P<pk>\d+)$', views.ProjeAlanlariDetailView.as_view(), name='projealanlari-detail'),
    #url(r'^projealanlari/create/$', views.ProjeAlanlariCreate.as_view(), name='projealanlari_create'),
    url(r'^projealanlari/create/$', views.projealanlari_yarat, name='projealanlari_yarat'),
    url(r'^projealanlari/(?P<pk>\d+)/update/$', views.ProjeAlanlariUpdate.as_view(), name='projealanlari_update'),
    url(r'^projealanlari/(?P<pk>\d+)/delete/$', views.projealanlari_sil, name='projealanlari_sil'),
    url(r'^projealanlari/(?P<pk>\d+)/delete/kesin/$', views.projealanlari_sil_kesin, name='projealanlari_sil_kesin'),

    # rfid dosyası - ws olmayan -  urlleri aşağıda....
    url(r'^rfid/$', views.rfid_dosyasi_listele, name='rfid_dosyasi_listele'),
    url(r'^rfid/(?P<pk>\d+)$', views.rfid_dosyasi_detay, name='rfid_dosyasi_detay'),
    url(r'^rfid/create/$', views.rfid_dosyasi_yarat, name='rfid_dosyasi_yarat'),
    url(r'^rfid/(?P<pk>\d+)/update/$', views.rfid_dosyasi_duzenle, name='rfid_dosyasi_duzenle'),
    url(r'^rfid/(?P<pk>\d+)/delete/$', views.rfid_dosyasi_sil, name='rfid_dosyasi_sil'),
    url(r'^rfid/(?P<pk>\d+)/delete/kesin/$', views.rfid_dosyasi_sil_kesin, name='rfid_dosyasi_sil_kesin'),

    # yer urlleri aşağıda....
    url(r'^yer/$', views.yer_listele, name='yer_listele'),
    #url(r'^yer/(?P<pk>\d+)$', views.yer_detay, name='yer_detay'),
    url(r'^yer/(?P<pk>\d+)$', views.yer_detay_gecici, name='yer_detay_gecici'),
    url(r'^yer/(?P<pk>\d+)/zaman_planla/$', views.yer_zaman_planla, name='yer_zaman_planla'),
    url(r'^yer/(?P<pk>\d+)/denetim_planla/$', views.yer_denetim_planla, name='yer_denetim_planla'),
    url(r'^yer/(?P<pk>\d+)/zaman_duzenle/$', views.yer_zaman_duzenle, name='yer_zaman_duzenle'),
    url(r'^yer/(?P<pk>\d+)/zaman_duzenle/js/$', views.yer_zaman_duzenle_js, name='yer_zaman_duzenle_js'),
    url(r'^yer/(?P<pk>\d+)/zaman_duzenle/create/$', views.yer_zaman_duzenle_create, name='yer_zaman_duzenle_create'),
    url(r'^yer/(?P<pk>\d+)/zaman_duzenle/update/$', views.yer_zaman_duzenle_update, name='yer_zaman_duzenle_update'),
    url(r'^yer/(?P<pk>\d+)/zaman_duzenle/delete/$', views.yer_zaman_duzenle_delete, name='yer_zaman_duzenle_delete'),
    url(r'^yer/(?P<pk>\d+)/zaman_duzenle/delete/kesin/$', views.yer_zaman_duzenle_kesin, name='yer_zaman_duzenle_kesin'),
    url(r'^yer/(?P<pk>\d+)/denetim_duzenle/$', views.yer_denetim_duzenle, name='yer_denetim_duzenle'),
    #url(r'^yer/create/$', views.YerCreate.as_view(), name='yer_create'),
    url(r'^yer/create/$', views.yer_yarat, name='yer_yarat'),
    #url(r'^yer/(?P<pk>\d+)/update/$', views.YerUpdate.as_view(), name='yer_update'),
    url(r'^yer/(?P<pk>\d+)/update/$', views.yer_duzenle, name='yer_duzenle'),
    url(r'^yer/(?P<pk>\d+)/delete/$', views.yer_sil, name='yer_sil'),
    url(r'^yer/(?P<pk>\d+)/delete/kesin/$', views.yer_sil_kesin, name='yer_sil_kesin'),


    # mk için olan url ler
    url(r'^mk_projealanlari/$', views.mk_projealanlari_listele, name='mk_projealanlari_listele'),
    url(r'^mk_yer/$', views.mk_yer_listele, name='mk_yer_proje_listele'),
    url(r'^mk_rfid/$', views.mk_rfid_listele, name='mk_rfid_proje_listele'),
    url(r'^mk_memnuniyet_list/$', views.mk_memnuniyet_list, name='mk_memnuniyet_list'),
    url(r'^mk_operasyon_list/$', views.mk_operasyon_list, name='mk_operasyon_list'),
    url(r'^mk_den_saha_list/$', views.mk_den_saha_list, name='mk_den_saha_list'),
    url(r'^mk_ariza_list/$', views.mk_ariza_list, name='mk_ariza_list'),



    # qrcode urlleri aşağıda....""
    url(r'^qrdosyasi/$', views.QrdosyasiListView.as_view(), name='qrdosyasi'),
    url(r'^qrdosyasi/(?P<pk>\d+)$', views.QrdosyasiDetailView.as_view(), name='qrdosyasi-detail'),
    url(r'^qrdosyasi/create/$', views.qrdosyasi_create, name='qrdosyasi_create'),
    url(r'^qrdosyasi/(?P<pk>\d+)/update/$', views.qrdosyasi_update, name='qrdosyasi_update'),
    url(r'^qrdosyasi/(?P<pk>\d+)/delete/$', views.qrdosyasi_sil, name='qrdosyasi_sil'),
    url(r'^qrdosyasi/(?P<pk>\d+)/delete/kesin/$', views.qrdosyasi_sil_kesin, name='qrdosyasi_sil_kesin'),

    url(r'^cagir1/$', views.cagir1, name='cagir1'),
    url(r'^cagir2/$', views.cagir2, name='cagir2'),
    url(r'^cagir3/$', views.cagir3, name='cagir3'),
    url(r'^cagir4/$', views.cagir4, name='cagir4'),

    url(r'^notification/$', views.list_notification, name='list_notification'),
    url(r'^notification/show/(?P<notification_id>\d+)/$', views.show_notification, name='show_notification'),
    url(r'^notification/delete/(?P<notification_id>\d+)/(?P<page_id>\d+)/$', views.delete_notification, name='delete_notification'),
    url(r'^notification/create/$', views.create_notification, name='create_notification'),


    ]
