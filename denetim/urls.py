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
from django.conf.urls import url, include
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
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^islem/', include('islem.urls')),
    url(r'^notification/', include('notification.urls')),
    url(r'^charts/', include('charts.urls')),
    #url(r'^rfid/', include('webservice.urls')),
    url(r'^ws/', include('webservice.api.urls', namespace='api-ws')),
    url(r'^bildirim/', views.bildirim, name='bildirim'),
    url(r'^popup_notif/', views.popup_notif, name='popup_notif'),
    #url(r'^pdf1/', views.GeneratePdf.as_view(), name='GeneratePdf'),
    url(r'^pdf1/', views.GeneratePDF.as_view(), name='GeneratePDF'),
    url(r'^pdf2/(?P<pk>\d+)$', views.Generate_Rapor_PDF.as_view(), name='Generate_Rapor_PDF'),
    #url(r'^pdf2/', views.generate_pdf, name='generate_pdf'),
    #url(r'^pdf2/', views.get_report, name='get_report'),
    url(r'^pdf2/', views.report_example, name='report_example'),
    url(r'^select2/', include('django_select2.urls')),
    #url(r'^select2/', include('select2.urls')),
    url(r'^xyz/', views.xyz, name='xyz'),
    url(r'^abc/', views.kamera, name='kamera'),
    url(r'^eposta/', views.eposta_gonder, name='eposta_gonder'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url('^searchableselect/', include('searchableselect.urls')),
    #url(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^report_builder/', include('report_builder.urls')),



handler400 = 'islem.views.my_400_bad_request_view'
handler403 = 'islem.views.my_403_permission_denied_view'
handler404 = 'islem.views.my_404_page_not_found_view'
handler500 = 'islem.views.my_500_error_view'
