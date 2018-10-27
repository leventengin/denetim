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
from django.conf.urls import url
from django.contrib import admin

from .views import HomeView, get_data, get_data_krs, ChartData
from .views import gunluk_yer, gunluk_yer_mem, gunluk_yer_opr, gunluk_yer_den, gunluk_yer_arz, gunluk_yer_say


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^api/data/$', get_data, name='api-data'),
    url(r'^api/data_krs/$', get_data_krs, name='api-data-krs'),
    url(r'^api/gunluk_yer/$', gunluk_yer, name='gunluk_yer'),
    url(r'^api/gunluk_yer_mem/$', gunluk_yer_mem, name='gunluk_yer_mem'),
    url(r'^api/gunluk_yer_den/$', gunluk_yer_den, name='gunluk_yer_den'),
    url(r'^api/gunluk_yer_opr/$', gunluk_yer_opr, name='gunluk_yer_opr'),
    url(r'^api/gunluk_yer_arz/$', gunluk_yer_arz, name='gunluk_yer_arz'),
    url(r'^api/gunluk_yer_say/$', gunluk_yer_say, name='gunluk_yer_say'),
    url(r'^api/chart/data/$', ChartData.as_view()),
    #url(r'^admin/', admin.site.urls),

]
