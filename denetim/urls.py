"""denetim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#from django.conf.urls import url, include
from django.urls import re_path, path, include
from django.contrib import admin
from islem import views
from django.conf import settings
from django.conf.urls.static import static
from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)





urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^islem/', include('islem.urls')),
    re_path(r'^notification/', include('notification.urls')),
    re_path(r'^charts/', include('charts.urls')),
    #re_path(r'^rfid/', include('webservice.urls')),
    re_path(r'^ws/', include('webservice.api.urls')),
    re_path(r'^bildirim/', views.bildirim, name='bildirim'),
    re_path(r'^popup_notif/', views.popup_notif, name='popup_notif'),
    #re_path(r'^pdf1/', views.GeneratePdf.as_view(), name='GeneratePdf'),
    re_path(r'^pdf1/', views.GeneratePDF.as_view(), name='GeneratePDF'),
    re_path(r'^pdf2/(?P<pk>\d+)$', views.Generate_Rapor_PDF.as_view(), name='Generate_Rapor_PDF'),
    #re_path(r'^pdf2/', views.generate_pdf, name='generate_pdf'),
    #re_path(r'^pdf2/', views.get_report, name='get_report'),
    re_path(r'^pdf2/', views.report_example, name='report_example'),
    re_path(r'^select2/', include('django_select2.urls')),
    #re_path(r'^select2/', include('select2.urls')),
    re_path(r'^xyz/', views.xyz, name='xyz'),
    re_path(r'^abc/', views.kamera, name='kamera'),
    re_path(r'^eposta/', views.eposta_gonder, name='eposta_gonder'),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path('^searchableselect/', include('searchableselect.urls')),
    #re_path(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    #re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #re_path(r'^report_builder/', include('report_builder.urls')),



handler400 = 'islem.views.my_400_bad_request_view'
handler403 = 'islem.views.my_403_permission_denied_view'
handler404 = 'islem.views.my_404_page_not_found_view'
handler500 = 'islem.views.my_500_error_view'
