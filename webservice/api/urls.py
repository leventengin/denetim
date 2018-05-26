

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

from .views import BlogPostRudView, BlogPostAPIView, BlogPostDestroyView, BlogPostDetailView
from .views import MacPostRudView, MacList, MacDetail, MacPostDetailView, Mac_Bul, Mac_Query, Mac_Filter
from .views import MemnuniyetRudView, MemnuniyetList, MemnuniyetDetail, MemnuniyetDetailView, MemnuniyetBul, MemnuniyetQuery, MemnuniyetFilter
from .views import OperasyonRudView, OperasyonList, OperasyonDetail, OperasyonDetailView, OperasyonBul, OperasyonQuery, OperasyonFilter
from .views import DenetimRudView, DenetimList, DenetimDetail, DenetimDetailView, DenetimBul, DenetimQuery, DenetimFilter
from .views import ArizaRudView, ArizaList, ArizaDetail, ArizaDetailView, ArizaBul, ArizaQuery, ArizaFilter
from .views import RfidRudView, RfidList, RfidDetail, RfidDetailView, RfidBul, RfidQuery, RfidFilter
from .views import YerudRudView, YerudList, YerudDetail, YerudDetailView, YerudBul, YerudQuery, YerudFilter

urlpatterns = [
    url(r'^auth/login/$', obtain_jwt_token, name='api-login'),
    url(r'^blogpost/$', BlogPostAPIView.as_view(), name='post-listcreate'),
    url(r'^blogpost/(?P<pk>\d+)/$', BlogPostRudView.as_view(), name='post-rud'),
    url(r'^blogpost/destroy/(?P<pk>\d+)/$', BlogPostDestroyView.as_view(), name='post-destroy'),
    url(r'^blogpost/bul/(?P<pk>\d+)/$', BlogPostDetailView.as_view(), name='bul_event'),
    url(r'^blogpost/bul/delete/(?P<pk>\d+)/$', BlogPostDetailView.as_view(), name='delete_event'),

    url(r'^mac_list/$', MacList.as_view(), name='mac_list'),
    url(r'^mac_bul/$', Mac_Bul.as_view(), name='mac_bul'),
    url(r'^mac_detail/(?P<pk>[0-9]+)/$', MacDetail.as_view(), name='mac-rud'),
    url(r'^mac_query/$', Mac_Query.as_view(), name='mac_query'),
    url(r'^mac_filtrele/(?P<mac_no>.+)/$', Mac_Filter.as_view(), name='mac_filter'),

    url(r'^memnuniyet_list/$', MemnuniyetList.as_view(), name='memnuniyet_list'),
    url(r'^memnuniyet_bul/$', MemnuniyetBul.as_view(), name='memnuniyet_bul'),
    url(r'^memnuniyet_detail/(?P<pk>[0-9]+)/$', MemnuniyetDetail.as_view(), name='memnuniyet-rud'),
    url(r'^memnuniyet_query/$', MemnuniyetQuery.as_view(), name='memnuniyet_query'),
    url(r'^memnuniyet_filtrele/(?P<mac_no>.+)/$', MemnuniyetFilter.as_view(), name='memnuniyet_filter'),

    url(r'^operasyon_list/$', OperasyonList.as_view(), name='operasyon_list'),
    url(r'^operasyon_bul/$', OperasyonBul.as_view(), name='operasyon_bul'),
    url(r'^operasyon_detail/(?P<pk>[0-9]+)/$', OperasyonDetail.as_view(), name='operasyon-rud'),
    url(r'^operasyon_query/$', OperasyonQuery.as_view(), name='operasyon_query'),
    url(r'^operasyon_filtrele/(?P<mac_no>.+)/$', OperasyonFilter.as_view(), name='operasyon_filter'),

    url(r'^denetim_list/$', DenetimList.as_view(), name='denetim_list'),
    url(r'^denetim_bul/$', DenetimBul.as_view(), name='denetim_bul'),
    url(r'^denetim_detail/(?P<pk>[0-9]+)/$', DenetimDetail.as_view(), name='denetim-rud'),
    url(r'^denetim_query/$', DenetimQuery.as_view(), name='denetim_query'),
    url(r'^denetim_filtrele/(?P<mac_no>.+)/$', DenetimFilter.as_view(), name='denetim_filter'),

    url(r'^ariza_list/$', ArizaList.as_view(), name='ariza_list'),
    url(r'^ariza_bul/$', ArizaBul.as_view(), name='ariza_bul'),
    url(r'^ariza_detail/(?P<pk>[0-9]+)/$', ArizaDetail.as_view(), name='ariza-rud'),
    url(r'^ariza_query/$', ArizaQuery.as_view(), name='ariza_query'),
    url(r'^ariza_filtrele/(?P<mac_no>.+)/$', ArizaFilter.as_view(), name='ariza_filter'),

    url(r'^rfid_list/$', RfidList.as_view(), name='rfid_list'),
    url(r'^rfid_bul/$', RfidBul.as_view(), name='rfid_bul'),
    url(r'^rfid_detail/(?P<pk>[0-9]+)/$', RfidDetail.as_view(), name='rfid-rud'),
    url(r'^rfid_query/$', RfidQuery.as_view(), name='rfid_query'),
    url(r'^rfid_filtrele/(?P<mac_no>.+)/$', RfidFilter.as_view(), name='rfid_filter'),

    url(r'^yerud_list/$', YerudList.as_view(), name='yerud_list'),
    url(r'^yerud_bul/$', YerudBul.as_view(), name='yerud_bul'),
    url(r'^yerud_detail/(?P<pk>[0-9]+)/$', YerudDetail.as_view(), name='yerud-rud'),
    url(r'^yerud_query/$', YerudQuery.as_view(), name='yerud_query'),
    url(r'^yerud_filtrele/(?P<mac_no>.+)/$', YerudFilter.as_view(), name='yerud_filter'),




]
