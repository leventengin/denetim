#from django.conf.urls import include, url
from django.urls import re_path, path, include
from . import views

urlpatterns = [
    #re_path(r'^$', views.list_notification, name='list_notification'),
    re_path(r'^show/(?P<notification_id>\d+)/$', views.show_notification, name='show_notification'),
    re_path(r'^delete/(?P<notification_id>\d+)/$', views.delete_notification, name='delete_notification'),
    re_path(r'^create/$', views.create_notification, name='create_notification'),
    re_path(r'^list/$', views.list_notification, name='list_notification'),
    ]
