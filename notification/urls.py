from django.conf.urls import include, url
from . import views

urlpatterns = [
    #url(r'^$', views.list_notification, name='list_notification'),
    url(r'^show/(?P<notification_id>\d+)/$', views.show_notification, name='show_notification'),
    url(r'^delete/(?P<notification_id>\d+)/$', views.delete_notification, name='delete_notification'),
    url(r'^create/$', views.create_notification, name='create_notification'),
    url(r'^list/$', views.list_notification, name='list_notification'),
    ]
