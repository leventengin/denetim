
from django.views.generic import RedirectView
from django.views.generic import View
from django.conf.urls import include, url
from . import views
from django.utils.translation import gettext as _
from rest_framework import routers, serializers, viewsets
# from django.contrib.auth import views
from django.conf.urls import include

urlpatterns = [
    url(r'^$', views.index, name='index'),


    url(r'^gozlemci/$', views.gozlemci_sec, name='gozlemci_sec'),
    url(r'^denetim/(?P<pk>\d+)$', views.denetim_detay, name='denetim_detay'),
    #url(r'^denetim/(?P<pk>\d+)/pdf/$', views.GeneratePDF.as_view(), name='GeneratePDF'),
    url(r'^denetim/(?P<pk>\d+)/pdf/$', views.generate_pdf, name='generate_pdf'),
    url(r'^baslat/$', views.denetim_baslat, name='denetim_baslat'),
    url(r'^baslat/kesin/$', views.denetim_baslat_kesin, name='denetim_baslat_kesin'),
    url(r'^baslat/devam/$', views.denetim_bolum_sec, name='denetim_bolum_sec'),
    url(r'^baslat/devam/secilen_bolumu_kaydet/$', views.secilen_bolumu_kaydet, name='secilen_bolumu_kaydet'),
    url(r'^baslat/devam/detay_islemleri_baslat/$', views.detay_islemleri_baslat, name='detay_islemleri_baslat'),
    url(r'^baslat/devam/denetim_detay_islemleri/$', views.denetim_detay_islemleri, name='denetim_detay_islemleri'),



#-------------------------------------------------------------------------------------------------
    # grup urlleri aşağıda....

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

    # müşteri urlleri aşağıda....
    url(r'^musteri/$', views.MusteriListView.as_view(), name='musteri'),
    url(r'^musteri/(?P<pk>\d+)$', views.MusteriDetailView.as_view(), name='musteri-detail'),
    url(r'^musteri/create/$', views.MusteriCreate.as_view(), name='musteri_create'),
    url(r'^musteri/(?P<pk>\d+)/update/$', views.MusteriUpdate.as_view(), name='musteri_update'),
    url(r'^musteri/(?P<pk>\d+)/delete/$', views.musteri_sil, name='musteri_sil'),
    url(r'^musteri/(?P<pk>\d+)/delete/kesin/$', views.musteri_sil_kesin, name='musteri_sil_kesin'),

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




    ]
