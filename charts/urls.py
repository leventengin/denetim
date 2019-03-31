"""charts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
#from django.conf.urls import url
from django.urls import re_path, path, include
from django.contrib import admin

from .views import HomeView, get_data, get_data_krs, ChartData, spv_ort_sonuc, denetci_ort_sonuc
from .views import gunluk_yer_mem, gunluk_yer_opr, gunluk_yer_den, gunluk_yer_arz, gunluk_yer_say


urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home'),
    re_path(r'^api/data/$', get_data, name='api-data'),
    re_path(r'^api/data_krs/$', get_data_krs, name='api-data-krs'),
    #re_path(r'^api/gunluk_yer/$', gunluk_yer, name='gunluk_yer'),
    re_path(r'^api/gunluk_yer_mem/$', gunluk_yer_mem, name='gunluk_yer_mem'),
    re_path(r'^api/gunluk_yer_den/$', gunluk_yer_den, name='gunluk_yer_den'),
    re_path(r'^api/gunluk_yer_opr/$', gunluk_yer_opr, name='gunluk_yer_opr'),
    re_path(r'^api/gunluk_yer_arz/$', gunluk_yer_arz, name='gunluk_yer_arz'),
    re_path(r'^api/gunluk_yer_say/$', gunluk_yer_say, name='gunluk_yer_say'),
    re_path(r'^api/spv_ort_sonuc/$', spv_ort_sonuc, name='spv_ort_sonuc'),
    re_path(r'^api/denetci_ort_sonuc/$', denetci_ort_sonuc, name='denetci_ort_sonuc'),
    re_path(r'^api/chart/data/$', ChartData.as_view()),
    #re_path(r'^admin/', admin.site.urls),

]
