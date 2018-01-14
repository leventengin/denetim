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

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('resimyukle_rest.urls', namespace='api')),
    url(r'^islem/', include('islem.urls')),
    #url(r'^pdf1/', views.GeneratePdf.as_view(), name='GeneratePdf'),
    url(r'^pdf1/', views.GeneratePDF.as_view(), name='GeneratePDF'),
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
