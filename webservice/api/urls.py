from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

from .views import BlogPostRudView, BlogPostAPIView, BlogPostDestroyView, BlogPostDetailView
from .views import MacPostRudView, MacList, MacDetail, MacPostDetailView, Mac_Bul, Mac_Query, Mac_Filter
from .views import MemnuniyetRudView, MemnuniyetList, MemnuniyetDetail, MemnuniyetDetailView, MemnuniyetBul, MemnuniyetQuery, MemnuniyetFilter



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

]


#url(r'^denetim/(?P<pk>\d+)/update/$', views.DenetimUpdate.as_view(), name='denetim_update'),
