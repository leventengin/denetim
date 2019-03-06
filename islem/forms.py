
from django import forms
from django.forms import ModelForm
from islem.models import Profile, grup, sirket, proje, tipi, bolum, detay, acil, sonuc_resim, eleman, User
from islem.models import sonuc_bolum, denetim, kucukresim, zon, plan_opr_gun, plan_den_gun, yer, proje_alanlari
from webservice.models import rfid_dosyasi
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User, Group
#from __future__ import unicode_literals
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.urls import reverse
from django.db.models import Q
from bootstrap_datepicker.widgets import DatePicker
import datetime
from datetime import date
from django.contrib.auth.models import User
from flask import request
from django.core import serializers
from django.contrib.postgres.search import SearchVector
from django.views.generic import FormView
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from datetime import date, datetime
from django.template.loader import render_to_string
import requests

from django import forms
from .models import sonuc_detay
from webservice.models import yer_updown
from django.contrib.admin.widgets import FilteredSelectMultiple

from functools import reduce
from itertools import chain
from pickle import PicklingError

from django import forms
from dal import autocomplete
from django.core import signing
from django.db.models import Q
from django.forms.models import ModelChoiceIterator
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy  as _lazy
from django.utils.encoding import force_text
from django.contrib.auth import password_validation
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError



OPERASYONDIGER = (
('O', _lazy('Operation')),
('T', _lazy('Technic')),
('D', _lazy('Project Management')),
)

EVETHAYIR = (
('E', _lazy('Yes')),
('H', _lazy('No')),
)

GUNLER = (
('Pzt', _lazy('Monday')),
('Sal', _lazy('Tuesday')),
('Çar', _lazy('Wednesday')),
('Per', _lazy('Thursday')),
('Cum', _lazy('Friday')),
('Cmt', _lazy('Saturday')),
('Paz', _lazy('Sunday')),
)


RUTINPLANLI = (
('P', _lazy('Planned')),
('R', _lazy('Routine')),
('S', _lazy('Ordered')),
('C', _lazy('Checklist')),
('D', _lazy('Operation')),
)

PUANLAMA_TURU = (
('A', _lazy('Ten based')),
('B', _lazy('Five based')),
('C', _lazy('Two based')),
)

ONLUK = (
('0', '0'),
('1', '1'),
('2', '2'),
('3', '3'),
('4', '4'),
('5', '5'),
('6', '6'),
('7', '7'),
('8', '8'),
('9', '9'),
('10', '10'),
)

BESLIK = (
('0', '0'),
('1', '1'),
('2', '2'),
('3', '3'),
('4', '4'),
('5', '5'),
)

IKILIK = (
('0', '0'),
('1', '1'),
)


class Denetim_Deneme_Form(forms.Form):
    denetim = forms.ModelChoiceField(queryset=denetim.objects.all(),
                 widget=autocomplete.ModelSelect2(url='denetim-autocomplete'), required=False)

    def clean(self):
        cleaned_data = super(Denetim_Deneme_Form, self).clean()
        cc_denetim = cleaned_data.get("denetim")
        print("cc denetim ..:", cc_denetim)

    @property
    def media(self):
        m_css = {"screen": ('admin/css/vendor/select2/select2.css',
                            'admin/css/autocomplete.css',
                            'autocomplete_light/select2.css',)
                            }
        m_js = [
            #'admin/js/vendor/jquery/jquery.js',
            'autocomplete_light/jquery.init.js',
            'admin/js/vendor/select2/select2.full.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/vendor/select2/dist/js/i18n/ru.js',
            'autocomplete_light/jquery.post-setup.js',
        ]
        return forms.Media(css = m_css, js = m_js)



class Denetim_Rutin_Baslat_Form(forms.Form):
    denetim = forms.ModelChoiceField(queryset=denetim.objects.all(),
                 widget=autocomplete.ModelSelect2(url='denetim-rutin-autocomplete'), required=False)

    @property
    def media(self):
        m_css = {"screen": ('admin/css/vendor/select2/select2.css',
                            'admin/css/autocomplete.css',
                            'autocomplete_light/select2.css',)
                            }
        m_js = [
            #'admin/js/vendor/jquery/jquery.js',
            'autocomplete_light/jquery.init.js',
            'admin/js/vendor/select2/select2.full.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/vendor/select2/dist/js/i18n/ru.js',
            'autocomplete_light/jquery.post-setup.js',
        ]
        return forms.Media(css = m_css, js = m_js)



class Den_Olustur_Form(forms.Form):
    denetim = forms.ModelChoiceField(queryset=denetim.objects.all(),
                 widget=autocomplete.ModelSelect2(url='denolustur-autocomplete'), required=False)


    @property
    def media(self):
        m_css = {"screen": ('admin/css/vendor/select2/select2.css',
                            'admin/css/autocomplete.css',
                            'autocomplete_light/select2.css',)
                            }
        m_js = [
            #'admin/js/vendor/jquery/jquery.js',
            'autocomplete_light/jquery.init.js',
            'admin/js/vendor/select2/select2.full.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/vendor/select2/dist/js/i18n/ru.js',
            'autocomplete_light/jquery.post-setup.js',
        ]
        return forms.Media(css = m_css, js = m_js)





class Qrcode_Form(forms.Form):
    denetim = forms.ModelChoiceField(queryset=denetim.objects.all(),
                 widget=autocomplete.ModelSelect2(url='rutindenetim-autocomplete'), required=False)
    qrcode = forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '40'}))

    @property
    def media(self):
        m_css = {"screen": ('admin/css/vendor/select2/select2.css',
                            'admin/css/autocomplete.css',
                            'autocomplete_light/select2.css',)
                            }
        m_js = [
            #'admin/js/vendor/jquery/jquery.js',
            'autocomplete_light/jquery.init.js',
            'admin/js/vendor/select2/select2.full.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/vendor/select2/dist/js/i18n/ru.js',
            'autocomplete_light/jquery.post-setup.js',
        ]
        return forms.Media(css = m_css, js = m_js)


class Ikili_Deneme_Form(forms.Form):
    denetim_deneme = forms.ModelChoiceField(queryset=denetim.objects.all(),
         widget=autocomplete.ModelSelect2(url='denetim-autocomplete'), required=False)
    sonuc_bolum_deneme = forms.ModelChoiceField(queryset=sonuc_bolum.objects.all(),
         widget=autocomplete.ModelSelect2(url='sonucbolum-autocomplete', forward=['denetim_deneme']  ), required=False)

    @property
    def media(self):
        m_css = {"screen": ('admin/css/vendor/select2/select2.css',
                            'admin/css/autocomplete.css',
                            'autocomplete_light/select2.css',)
                            }
        m_js = [
            #'admin/js/vendor/jquery/jquery.js',
            'autocomplete_light/jquery.init.js',
            'admin/js/vendor/select2/select2.full.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/vendor/select2/dist/js/i18n/ru.js',
            'autocomplete_light/jquery.post-setup.js',
        ]
        return forms.Media(css = m_css, js = m_js)


class ProjeSecForm(forms.Form):
    proje = forms.ModelChoiceField(queryset=proje.objects.all(),
                 widget=autocomplete.ModelSelect2(url='proje-autocomplete'), required=False)

    @property
    def media(self):
        m_css = {"screen": ('admin/css/vendor/select2/select2.css',
                            'admin/css/autocomplete.css',
                            'autocomplete_light/select2.css',)
                            }
        m_js = [
            #'admin/js/vendor/jquery/jquery.js',
            'autocomplete_light/jquery.init.js',
            'admin/js/vendor/select2/select2.full.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/vendor/select2/dist/js/i18n/ru.js',
            'autocomplete_light/jquery.post-setup.js',
        ]
        return forms.Media(css = m_css, js = m_js)




class SirketSecForm(forms.Form):
    sirket = forms.ModelChoiceField(queryset=sirket.objects.all(),
                 widget=autocomplete.ModelSelect2(url='sirket2-autocomplete'), required=False)

    @property
    def media(self):
        m_css = {"screen": ('admin/css/vendor/select2/select2.css',
                            'admin/css/autocomplete.css',
                            'autocomplete_light/select2.css',)
                            }
        m_js = [
            #'admin/js/vendor/jquery/jquery.js',
            'autocomplete_light/jquery.init.js',
            'admin/js/vendor/select2/select2.full.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/vendor/select2/dist/js/i18n/ru.js',
            'autocomplete_light/jquery.post-setup.js',
        ]
        return forms.Media(css = m_css, js = m_js)



class SoruListesiForm(forms.Form):
    tipi = forms.ModelChoiceField(queryset=tipi.objects.all(),
         widget=autocomplete.ModelSelect2(url='list_tipi-autocomplete'), required=False)
    zon = forms.ModelChoiceField(queryset=zon.objects.all(),
         widget=autocomplete.ModelSelect2(url='list_zon-autocomplete', forward=['tipi'] ), required=False)
    bolum = forms.ModelChoiceField(queryset=bolum.objects.all(),
         widget=autocomplete.ModelSelect2(url='list_bolum-autocomplete', forward=['zon'] ), required=False)

    def clean(self):
        cleaned_data = super(SoruListesiForm, self).clean()
        cc_tipi = cleaned_data.get("tipi")
        cc_zon = cleaned_data.get("zon")
        cc_bolum = cleaned_data.get("bolum")
        print("cc tipi...", cc_tipi)
        print("cc zon....", cc_zon)
        print("cc bölüm....", cc_bolum)

        if cc_tipi == None:
            raise forms.ValidationError("denetim tipi alanı boş olamaz")
        if cc_zon == None:
            raise forms.ValidationError("denetim zonu alanı boş olamaz")
        if cc_bolum == None:
            raise forms.ValidationError("denetim bölümü alanı boş olamaz")

    @property
    def media(self):
        m_css = {"screen": ('admin/css/vendor/select2/select2.css',
                            'admin/css/autocomplete.css',
                            'autocomplete_light/select2.css',)
                            }
        m_js = [
            #'admin/js/vendor/jquery/jquery.js',
            'autocomplete_light/jquery.init.js',
            'admin/js/vendor/select2/select2.full.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/vendor/select2/dist/js/i18n/ru.js',
            'autocomplete_light/jquery.post-setup.js',
        ]
        return forms.Media(css = m_css, js = m_js)



class BolumListesiForm(forms.Form):
    tipi = forms.ModelChoiceField(queryset=tipi.objects.all(),
         widget=autocomplete.ModelSelect2(url='list_tipi-autocomplete'), required=False)
    zon = forms.ModelChoiceField(queryset=zon.objects.all(),
         widget=autocomplete.ModelSelect2(url='list_zon-autocomplete', forward=['tipi'] ), required=False)

    def clean(self):
        cleaned_data = super(BolumListesiForm, self).clean()
        cc_tipi = cleaned_data.get("tipi")
        cc_zon = cleaned_data.get("zon")
        print("cc tipi...", cc_tipi)
        print("cc zon....", cc_zon)
        if cc_tipi == None:
            raise forms.ValidationError("denetim tipi alanı boş olamaz")
        if cc_zon == None:
            raise forms.ValidationError("denetim zonu alanı boş olamaz")

    @property
    def media(self):
        m_css = {"screen": ('admin/css/vendor/select2/select2.css',
                            'admin/css/autocomplete.css',
                            'autocomplete_light/select2.css',)
                            }
        m_js = [
            #'admin/js/vendor/jquery/jquery.js',
            'autocomplete_light/jquery.init.js',
            'admin/js/vendor/select2/select2.full.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/vendor/select2/dist/js/i18n/ru.js',
            'autocomplete_light/jquery.post-setup.js',
        ]
        return forms.Media(css = m_css, js = m_js)



class ZonListesiForm(forms.Form):
    tipi = forms.ModelChoiceField(queryset=tipi.objects.all(),
         widget=autocomplete.ModelSelect2(url='list_tipi-autocomplete'), required=False)

    def clean(self):
        cleaned_data = super(ZonListesiForm, self).clean()
        cc_tipi = cleaned_data.get("tipi")
        print("cc tipi...", cc_tipi)
        if cc_tipi == None:
            raise forms.ValidationError("denetim tipi alanı boş olamaz")

    @property
    def media(self):
        m_css = {"screen": ('admin/css/vendor/select2/select2.css',
                            'admin/css/autocomplete.css',
                            'autocomplete_light/select2.css',)
                            }
        m_js = [
            #'admin/js/vendor/jquery/jquery.js',
            'autocomplete_light/jquery.init.js',
            'admin/js/vendor/select2/select2.full.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/vendor/select2/dist/js/i18n/ru.js',
            'autocomplete_light/jquery.post-setup.js',
        ]
        return forms.Media(css = m_css, js = m_js)

# esas işin döndüğü yer foto yüklüyor................
#
class SonucForm(forms.ModelForm):
    class Meta:
        model = sonuc_detay
        fields = ( 'puanlama_turu', 'onluk', 'beslik', 'ikilik', 'denetim_disi',  )
        """
        widgets = {
            'tamam' : forms.HiddenInput(),
        }
        """
        labels = {
            'denetim_disi' : "Denetim dışı",
            'onluk' : "Puan",
            'beslik': "Puan",
            'ikilik': "Puan",
        }
    def __init__(self, *args, **kwargs):
        super(SonucForm, self).__init__(*args, **kwargs)
        puanlama_turu = self.instance.puanlama_turu
        if puanlama_turu=="A":
            self.fields['beslik'].widget = forms.HiddenInput()
            self.fields['ikilik'].widget = forms.HiddenInput()
        if puanlama_turu=="B":
            self.fields['onluk'].widget = forms.HiddenInput()
            self.fields['ikilik'].widget = forms.HiddenInput()
        if puanlama_turu=="C":
            self.fields['onluk'].widget = forms.HiddenInput()
            self.fields['beslik'].widget = forms.HiddenInput()
        self.fields['puanlama_turu'].widget = forms.HiddenInput()


    def clean(self):
        cleaned_data = super(SonucForm, self).clean()
        cc_puanlama_turu = cleaned_data.get("puanlama_turu")
        cc_onluk = cleaned_data.get("onluk")
        cc_beslik = cleaned_data.get("beslik")
        cc_ikilik = cleaned_data.get("ikilik")
        cc_denetim_disi = cleaned_data.get("denetim_disi")
        print("cc puanlama türü...:", cc_puanlama_turu)
        print("cc onluk", cc_onluk)
        print("cc beslik", cc_beslik)
        print("cc ikilik", cc_ikilik)
        print("cc denetim dışı", cc_denetim_disi)


class SonucResimForm(forms.ModelForm):
    class Meta:
        model = sonuc_resim
        fields = ( 'sonuc_detay', 'foto',)

    def clean(self):
        cleaned_data = super(SonucResimForm, self).clean()
        cc_foto = cleaned_data.get("sonuc_detay")
        cc_foto = cleaned_data.get("foto")
        #cc_resim_kalktimi = cleaned_data.get("resim_kalktimi")
        print("cc sonuc detay...:", cc_sonuc_detay)
        print("cc foto...:", cc_foto)
        #print("cc resim kalkti mı", cc_resim_kalktimi)



class SoruForm(forms.Form):
    detay_kodu = forms.CharField(label='Detay Kodu:', widget=forms.TextInput(attrs={'class':'special', 'size': '10'}))
    detay_adi = forms.CharField(label='Detay Adı:', widget=forms.Textarea(attrs={'cols': 100, 'rows': 2}))
    puanlama_turu = forms.ChoiceField(choices=PUANLAMA_TURU, widget=forms.Select, label="Puanlama Türü:")
    def __init__(self, *args, **kwargs):
        super(SoruForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SoruForm, self).clean()
        cc_detay_kodu = cleaned_data.get("detay_kodu")
        cc_detay_adi = cleaned_data.get("detay_adi")
        cc_puanlama_turu = cleaned_data.get("puanlama_turu")
        print("cc detay kodu...", cc_detay_kodu)
        print("cc detay adı....", cc_detay_adi)
        print("cc puanlama türü", cc_puanlama_turu)




class BolumForm(forms.Form):
    bolum_kodu = forms.CharField(label='Bölüm Kodu:', widget=forms.TextInput(attrs={'class':'special', 'size': '10'}))
    bolum_adi = forms.CharField(label='Bölüm Adı:', widget=forms.Textarea(attrs={'cols': 100, 'rows': 1}))
    def __init__(self, *args, **kwargs):
        super(BolumForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(BolumForm, self).clean()
        cc_bolum_kodu = cleaned_data.get("bolum_kodu")
        cc_bolum_adi = cleaned_data.get("bolum_adi")
        print("cc detay kodu...", cc_bolum_kodu)
        print("cc detay adı....", cc_bolum_adi)


class ZonForm(forms.Form):
    zon_kodu = forms.CharField(label='Alan Kodu:', widget=forms.TextInput(attrs={'class':'special', 'size': '10'}))
    zon_adi = forms.CharField(label='Alan Adı:', widget=forms.Textarea(attrs={'cols': 100, 'rows': 1}))
    def __init__(self, *args, **kwargs):
        super(ZonForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ZonForm, self).clean()
        cc_zon_kodu = cleaned_data.get("zon_kodu")
        cc_zon_adi = cleaned_data.get("zon_adi")
        print("cc zon kodu...", cc_zon_kodu)
        print("cc zon adı....", cc_zon_adi)







class GunDenForm(forms.ModelForm):
    class Meta:
        model = plan_den_gun
        fields = ( 'gun', 'zaman',)
        labels = {
            'gun': "Gün giriniz",
            'zaman' : "Saat giriniz",
        }
        help_texts = {
            'gun': _("please enter the time in hh:mm:ss format (hour : minute : second) "),
        }

    def clean(self):
        cleaned_data = super(GunDenForm, self).clean()
        cc_gun = cleaned_data.get("gun")
        cc_zaman = cleaned_data.get("zaman")
        print("cc gun - cc zaman", cc_gun, "-", cc_zaman)

class GunForm(forms.ModelForm):
    class Meta:
        model = plan_opr_gun
        fields = ( 'gun', 'zaman',)
        labels = {
            'gun': "Gün giriniz",
            'zaman' : "Saat giriniz",
        }
        help_texts = {
            'gun': _("please enter the time in hh:mm:ss format (hour : minute : second) "),
        }

    def clean(self):
        cleaned_data = super(GunForm, self).clean()
        cc_gun = cleaned_data.get("gun")
        cc_zaman = cleaned_data.get("zaman")
        print("cc gun - cc zaman", cc_gun, "-", cc_zaman)


class SaatDenForm(forms.ModelForm):
    class Meta:
        model = plan_den_gun
        fields = ( 'zaman',)
        labels = {
            'zaman' : "Saat giriniz:",
        }
        help_texts = {
            'zaman': _("please enter the time in hh:mm:ss format (hour : minute : second) "),
        }
    def clean(self):
        cleaned_data = super(SaatDenForm, self).clean()
        cc_zaman = cleaned_data.get("zaman")
        print("cc zaman", cc_zaman)


class SaatForm(forms.ModelForm):
    class Meta:
        model = plan_opr_gun
        fields = ( 'zaman',)
        labels = {
            'zaman' : "Saat giriniz:",
        }
        help_texts = {
            'zaman': _("please enter the time in hh:mm:ss format (hour : minute : second) "),
        }
    def clean(self):
        cleaned_data = super(SaatForm, self).clean()
        cc_zaman = cleaned_data.get("zaman")
        print("cc zaman", cc_zaman)



class YerForm(forms.ModelForm):
    class Meta:
        model = yer
        fields = ( 'proje_alanlari', 'yer_adi', 'mac_no', 'opr_basl', 'opr_son', 'opr_delta', 'den_basl', 'den_son', 'den_delta', 'opr_sure',)
        labels = {
            'proje_alanlari' : 'Proje Alanı:',
            'yer_adi' : 'Yer Adı:',
            'mac_no': 'Mac No:',
            'opr_basl': 'Operasyon Başlangıç Saati:',
            'opr_son': 'Son Operasyon Saati:',
            'opr_delta': 'Operasyon Arası Süre:',
            'den_basl': 'Denetim Başlangıç Saati:',
            'den_son': 'Son Denetim Saati:',
            'den_delta': 'Denetim Arasi Süre:',
            'opr_sure': 'Öngörülen Operasyon Süresi:  ',
        }
        help_texts = {
            'mac_no': _('please enter the time in hh:mm:ss format (hour : minute : second) '),
        }
        error_messages = {
            'yer_adi': { 'required': _('Place name is missing..') },
        }


    def clean(self):
        cleaned_data = super(YerForm, self).clean()
        cc_pa = cleaned_data.get("proje_alanlari")
        print("proje alanları....", cc_pa)
        cc_yer_adi = cleaned_data.get("yer_adi")
        cc_mac_no = cleaned_data.get("mac_no")
        cc_opr_basl = cleaned_data.get("opr_basl")
        cc_opr_son = cleaned_data.get("opr_son")
        cc_opr_delta = cleaned_data.get("opr_delta")
        cc_den_basl = cleaned_data.get("den_basl")
        cc_den_son = cleaned_data.get("den_son")
        cc_den_delta = cleaned_data.get("den_delta")

    def __init__(self, *args, **kwargs):
        kullanici = kwargs.pop("kullanici")
        super(YerForm, self).__init__(*args, **kwargs)
        proje = kullanici.profile.proje
        print("işte yer form init içinden proje...")
        pa_obj = proje_alanlari.objects.filter(proje=proje)
        self.fields['proje_alanlari'].queryset = pa_obj



class PAForm(forms.ModelForm):
    class Meta:
        model = proje_alanlari
        fields = ( 'proje', 'alan', )
        labels = {
            'proje' : 'Proje Adı:',
            'alan' : 'Alan Adı:',
        }

    def clean(self):
        cleaned_data = super(PAForm, self).clean()
        cc_proje = cleaned_data.get("proje")
        cc_alan = cleaned_data.get("alan")

    def __init__(self, *args, **kwargs):
        kullanici = kwargs.pop("kullanici")
        super(PAForm, self).__init__(*args, **kwargs)
        prj = kullanici.profile.proje
        print("işte yer form init içinden proje...", prj)
        proje_obj = proje.objects.filter(id=prj.id)
        print("işte  proje objesi.....", proje_obj)
        self.fields['proje'].queryset = proje_obj


import re
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q


class RfidForm(forms.ModelForm):
    class Meta:
        model = rfid_dosyasi
        fields = ( 'rfid_no', 'proje', 'rfid_tipi', 'kullanici', 'eleman',)
        labels = {
            'rfid_no': 'RFID No',
            'proje' : 'Proje Adı:',
            'rfid_tipi' : 'RFID Tipi:',
            'kullanici': 'Kullanıcı:',
            'eleman': 'Çalışan',
        }


    def __init__(self, *args, **kwargs):
        kullan = kwargs.pop("kullan")
        super(RfidForm, self).__init__(*args, **kwargs)
        prj = kullan.profile.proje
        print("işte yer form init içinden proje...", prj)
        proje_obj = proje.objects.filter(id=prj.id)
        print("işte  proje objesi.....", proje_obj)
        self.fields['proje'].queryset = proje_obj
        profile_obj = Profile.objects.filter(proje=prj)
        p_list = []
        for prof in profile_obj:
            p_list.append(prof.user.id)
        print("kullancı id listesi...", p_list)
        usr_obj = User.objects.all()
        #usr_obj = User.objects.get(Q(id in p_list))
        usr_obj = usr_obj.filter(Q(id__in =  p_list))
        print("user object with p list...", usr_obj)
        self.fields['kullanici'].queryset = usr_obj
        eleman_obj = eleman.objects.filter(proje=prj).filter(aktifcalisan="E")
        self.fields['eleman'].queryset = eleman_obj

    def clean(self):
        cleaned_data = super(RfidForm, self).clean()
        rfid_no = cleaned_data.get('rfid_no')
        proje = cleaned_data.get('proje')
        rfid_tipi = cleaned_data.get('rfid_tipi')
        kullanici = cleaned_data.get('kullanici')
        eleman = cleaned_data.get('eleman')


        print("cc rfid no", rfid_no)
        print("cc proje", proje)
        print("cc rfid tipi", rfid_tipi)
        print("cc kullanici", kullanici)
        print("cc eleman", eleman)

        if (rfid_tipi == "D" or rfid_tipi == "T") and (kullanici == None):
            print("yoksa burada.........")
            raise forms.ValidationError("kullanıcı alanı boş olamaz...")
        if (rfid_tipi == "O") and (eleman == None):
            print("yoksa burada..222.......")
            raise forms.ValidationError("eleman alanı boş olamaz...")

        return cleaned_data





class ElemanForm(forms.ModelForm):
    class Meta:
        model = eleman
        fields = ( 'adi', 'soyadi', 'kull_adi', 'aktifcalisan')
        labels = {
            'adi': 'Adı:',
            'soyadi' : 'Soyadı:',
            'kull_adi' : 'Vatandaşlık No:',
            'aktifcalisan': 'Çalışma Durumu:'
        }

    def clean(self):
        cleaned_data = super(ElemanForm, self).clean()
        cc_adi = cleaned_data.get('adi')
        cc_soyadi = cleaned_data.get('soyadi')
        cc_kullanici = cleaned_data.get('kull_adi')

        print("cc adi", cc_adi)
        print("cc soyadi", cc_soyadi)
        print("cc soyadi", cc_kullanici)

        return cleaned_data






class VatandaslikForm(forms.Form):
    vatno = forms.CharField(label='Vatandaşlık No:', widget=forms.TextInput(attrs={'class':'special', 'size': '10'}))
    def clean(self):
        cleaned_data = super(VatandaslikForm, self).clean()
        cc_vatno = cleaned_data.get('vatno')
        print("cc vatno", cc_vatno)
        return cleaned_data




class AcilAcForm(forms.Form):
    denetim = forms.ModelChoiceField(queryset=denetim.objects.all(), label="Denetim Seçiniz..")
    konu = forms.CharField()
    aciklama = forms.CharField(label='Açıklama', widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}),)
    def __init__(self, *args, **kwargs):
        denetci = kwargs.pop("denetci")
        super(AcilAcForm, self).__init__(*args, **kwargs)
        denetim_obj_ilk = denetim.objects.filter(durum="B")
        denetim_obj = denetim_obj_ilk.filter(denetci=denetci)
        self.fields['denetim'].queryset = denetim_obj
        print("queryset initial içinden..:", self.fields['denetim'].queryset)


class AcilKapaForm(forms.Form):
    denetim = forms.ModelChoiceField(queryset=denetim.objects.all(), label="Denetim Seçiniz..")
    sonuc = forms.CharField(label='Sonuç', widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}),)
    def __init__(self, *args, **kwargs):
        denetci = kwargs.pop("denetci")
        super(AcilAcForm, self).__init__(*args, **kwargs)
        denetim_obj_ilk = denetim.objects.filter(durum="C")
        denetim_obj = denetim_obj_ilk.filter(denetci=denetci)
        self.fields['denetim'].queryset = denetim_obj
        print("queryset initial içinden..:", self.fields['denetim'].queryset)


class YerSecForm(forms.Form):
    tarih = forms.DateField(label='Tarih', required=False,
                        widget=forms.TextInput(attrs={ 'class':'datepicker' }))
    yersec = forms.ModelChoiceField(queryset=yer.objects.all(), label="Yer ")
    def __init__(self, *args, **kwargs):
        proje = kwargs.pop("proje")
        super(YerSecForm, self).__init__(*args, **kwargs)
        palan_obj = proje_alanlari.objects.filter(proje=proje)
        qs = yer.objects.none()
        for palan in palan_obj:
            qx = yer.objects.filter(proje_alanlari=palan)
            qs = qs.union(qx)
        self.fields['yersec'].queryset = qs
        print("queryset initial içinden..:", self.fields['yersec'].queryset)



class MacnoYerForm(forms.Form):
    macnoyer = forms.ModelChoiceField(queryset=yer_updown.objects.all(), label="Mac_no Seçiniz..")


class RfidProjeForm(forms.Form):
    proje = forms.ModelChoiceField(queryset=proje.objects.all(), label="Proje Seçiniz..")


class SirketIcinProjeForm(forms.Form):
    proje = forms.ModelChoiceField(queryset=proje.objects.all())
    def __init__(self, *args, **kwargs):
        sirket = kwargs.pop("sirket")
        super(SirketIcinProjeForm, self).__init__(*args, **kwargs)
        proje_obj = proje.objects.filter(sirket=sirket)
        self.fields['proje'].queryset = proje_obj
        print("queryset initial içinden..:", self.fields['proje'].queryset)




class DenetimForm(forms.Form):
    pk_no = forms.IntegerField(required=False, widget=forms.HiddenInput())
    denetim_adi = forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '50'}))
    proje = forms.ModelChoiceField(queryset=proje.objects.all(),
                     widget=autocomplete.ModelSelect2(url='proje-autocomplete'), required=False)
    rutin_planli = forms.ChoiceField(choices=RUTINPLANLI, widget=forms.RadioSelect, label="Planlı/Rutin")
    rp_hidden = forms.CharField(max_length=1, widget=forms.HiddenInput())
    denetci = forms.ModelChoiceField(queryset=Profile.objects.filter(denetci="E"),
                     widget=autocomplete.ModelSelect2(url='denetci-autocomplete'), required=False)
    tipi = forms.ModelChoiceField(queryset=tipi.objects.all(),
                 widget=autocomplete.ModelSelect2(url='tipi-autocomplete'), required=False)
    takipciler = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label='Takipçiler',
                widget=autocomplete.ModelSelect2Multiple(url='takipci-autocomplete'), required=False)
    hedef_baslangic = forms.DateField(label='Hedef başlangıç...:', required=False,
                        widget=forms.TextInput(attrs={ 'class':'datepicker' }))
    hedef_bitis = forms.DateField(label='Hedef bitiş...:', required=False,
                        widget=forms.TextInput(attrs={ 'class':'datepicker' }))
    aciklama = forms.CharField(label='Açıklama', widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}), required=False)
    #zonlar = forms.ModelMultipleChoiceField(queryset=zon.objects.all(), label='Zonlar............:',
    #             widget=autocomplete.ModelSelect2Multiple(url='zon-autocomplete', forward=['tipi'] ), required=False)
    bolum = forms.ModelMultipleChoiceField(queryset=bolum.objects.all(), label='Bölümler...............:',
                 widget=autocomplete.ModelSelect2Multiple(url='bolum-autocomplete', forward=['tipi'] ), required=False)
    detay = forms.ModelMultipleChoiceField(queryset=detay.objects.all(), label=None,
            widget=forms.CheckboxSelectMultiple(attrs={"checked":""}), required=False)

    def __init__(self, *args, **kwargs):
        bolum_listesi = kwargs.pop("bolum_listesi")
        #init_param = kwargs.pop("init_param")
        #detaylar = kwargs.pop("detaylar")
        super(DenetimForm, self).__init__(*args, **kwargs)
        print("init içinden seçilen bölüm listesi", bolum_listesi)
        #print("init param...", init_param)
        #print("init içinden detaylar....", detaylar)
        qs = detay.objects.none()
        if not (bolum_listesi == None):
            i = 0
            print("len...", len(bolum_listesi))
            while i < len(bolum_listesi):
                qx = detay.objects.filter(bolum=bolum_listesi[i]).filter(sil=False)
                print("qx...", qx)
                qs = qs.union(qx)
                i = i+1
        qs = qs.order_by('detay_kodu')
        print("qs.....", qs)
        self.fields['detay'].queryset = qs


    def clean(self):
        cleaned_data = super(DenetimForm, self).clean()
        cc_denetim_adi = cleaned_data.get("denetim_adi")
        cc_proje = cleaned_data.get("proje")
        cc_rutin_planli = cleaned_data.get("rutin_planli")
        cc_denetci = cleaned_data.get("denetci")
        cc_tipi = cleaned_data.get("tipi")
        cc_takipciler = cleaned_data.get("takipciler")
        cc_hedef_baslangic = cleaned_data.get("hedef_baslangic")
        cc_hedef_bitis = cleaned_data.get("hedef_bitis")
        cc_aciklama = cleaned_data.get("aciklama")
        cc_bolum = cleaned_data.get("bolum")
        cc_detay = cleaned_data.get("detay")
        print("cc denetim adı...:", cc_denetim_adi)
        print("cc proje", cc_proje)
        print("cc rutin planlı", cc_rutin_planli)
        print("cc denetçi...:", cc_denetci)
        print("cc tipi", cc_tipi)
        print("cc takipçiler", cc_takipciler)
        print("cc hedef başlangıç...:", cc_hedef_baslangic)
        print("cc hedef_bitis", cc_hedef_bitis)
        print("cc açıklama ", cc_aciklama)
        print("cc bolum", cc_bolum)
        print("cc detay", cc_detay)
        #conv_date_basla = cc_hedef_baslangic.date()
        #conv_date_bitis = cc_hedef_bitis.date()


        if (cc_rutin_planli == "P"):
            if (cc_hedef_baslangic == "" ) or (cc_hedef_baslangic == "" ):
                raise forms.ValidationError(
                        " tarihler boş olamaz.... ")
            if (cc_hedef_baslangic > cc_hedef_bitis):
                print("TARİH SIRALAMASI YANLIŞ...............")
                raise forms.ValidationError(" tarih sıralaması yanlış...")
        return self.cleaned_data


    @property
    def media(self):
        m_css = {"screen": ('admin/css/vendor/select2/select2.css',
                            'admin/css/autocomplete.css',
                            'autocomplete_light/select2.css',)
                            }
        m_js = [
            #'admin/js/vendor/jquery/jquery.js',
            'autocomplete_light/jquery.init.js',
            'admin/js/vendor/select2/select2.full.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/jquery.post-setup.js',
        ]
        return forms.Media(css = m_css, js = m_js)




class RaporTarihForm(forms.Form):
    hedef_baslangic = forms.DateField(label='Hedef başlangıç...:', required=False,
                        widget=forms.TextInput(attrs={ 'class':'datepicker' }))
    hedef_bitis = forms.DateField(label='Hedef bitiş...:', required=False,
                        widget=forms.TextInput(attrs={ 'class':'datepicker' }))

    def clean(self):
        cleaned_data = super(DenetimForm, self).clean()
        cc_hedef_baslangic = cleaned_data.get("hedef_baslangic")
        cc_hedef_bitis = cleaned_data.get("hedef_bitis")

        if (cc_hedef_baslangic == "" ) or (cc_hedef_baslangic == "" ):
            raise forms.ValidationError(" tarihler boş olamaz.... ")
        if (cc_hedef_baslangic > cc_hedef_bitis):
            raise forms.ValidationError(" tarih sıralaması yanlış...")
        if (cc_hedef_baslangic.date < datetime.today()):
            raise forms.ValidationError(" başlangıç için ileri bir tarih girmelisiniz.... ")
        if (cc_hedef_bitis < datetime.date.today()):
            raise forms.ValidationError(" bitiş için ileri bir tarih girmelisiniz.... ")
        return self.cleaned_data



class Sirket_Mem_RaporForm(forms.Form):
    proje = forms.ModelChoiceField(queryset=proje.objects.all())
    hedef_baslangic = forms.DateField(label='Hedef başlangıç...:', required=False,
                        widget=forms.TextInput(attrs={ 'class':'datepicker' }))
    hedef_bitis = forms.DateField(label='Hedef bitiş...:', required=False,
                        widget=forms.TextInput(attrs={ 'class':'datepicker' }))

    def __init__(self, *args, **kwargs):
        sirket = kwargs.pop("sirket")
        super(Sirket_Mem_RaporForm, self).__init__(*args, **kwargs)
        proje_obj = proje.objects.filter(sirket=sirket)
        self.fields['proje'].queryset = proje_obj
        print("queryset initial içinden..:", self.fields['proje'].queryset)

    def clean(self):
        cleaned_data = super(DenetimForm, self).clean()
        cc_hedef_baslangic = cleaned_data.get("hedef_baslangic")
        cc_hedef_bitis = cleaned_data.get("hedef_bitis")
        cc_proje = cleaned_data.get("proje")
        if (cc_hedef_baslangic == "" ) or (cc_hedef_baslangic == "" ):
            raise forms.ValidationError(" tarihler boş olamaz.... ")
        if (cc_hedef_baslangic > cc_hedef_bitis):
            raise forms.ValidationError(" tarih sıralaması yanlış...")
        if (cc_hedef_baslangic.date < datetime.today()):
            raise forms.ValidationError(" başlangıç için ileri bir tarih girmelisiniz.... ")
        if (cc_hedef_bitis < datetime.date.today()):
            raise forms.ValidationError(" bitiş için ileri bir tarih girmelisiniz.... ")
        return self.cleaned_data






class KucukResimForm(forms.ModelForm):
    class Meta:
        model = kucukresim
        fields = ('foto_kucuk',)


class SpvForm(forms.Form):
    spv = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label="Süpervizör",
                 widget=autocomplete.ModelSelect2Multiple(url='spv-autocomplete'), required=False)

    @property
    def media(self):
        m_css = {"screen": ('admin/css/vendor/select2/select2.css',
                            'admin/css/autocomplete.css',
                            'autocomplete_light/select2.css',)
                            }
        m_js = [
            #'admin/js/vendor/jquery/jquery.js',
            'autocomplete_light/jquery.init.js',
            'admin/js/vendor/select2/select2.full.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/vendor/select2/dist/js/i18n/ru.js',
            'autocomplete_light/jquery.post-setup.js',
        ]
        return forms.Media(css = m_css, js = m_js)

class DenForm(forms.Form):
    den = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label="Denetci",
                 widget=autocomplete.ModelSelect2Multiple(url='den-autocomplete'), required=False)

    @property
    def media(self):
        m_css = {"screen": ('admin/css/vendor/select2/select2.css',
                            'admin/css/autocomplete.css',
                            'autocomplete_light/select2.css',)
                            }
        m_js = [
            #'admin/js/vendor/jquery/jquery.js',
            'autocomplete_light/jquery.init.js',
            'admin/js/vendor/select2/select2.full.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/vendor/select2/dist/js/i18n/ru.js',
            'autocomplete_light/jquery.post-setup.js',
        ]
        return forms.Media(css = m_css, js = m_js)


#ilk bölümde detay işlemleri öncesinde denetim ve bölüm seçen form js ile...
class IkiliSecForm(forms.Form):
    denetim = forms.ModelChoiceField(queryset=denetim.objects.all(), label="Denetim Seçiniz..")
    bolum = forms.ModelChoiceField(queryset=sonuc_bolum.objects.all(), label="Bölüm Seçiniz..")
    def __init__(self, *args, **kwargs):
        kullanan = kwargs.pop("kullanan")
        denetim_no = kwargs.pop("denetim_no")
        super(IkiliSecForm, self).__init__(*args, **kwargs)
        print("form init içinden kullanan", kullanan)
        print("form init içinden denetim_no", denetim_no)
        denetim_obj_ilk = denetim.objects.filter(durum="A")
        denetim_obj = denetim_obj_ilk.filter(yaratan=kullanan)
        self.fields['denetim'].queryset = denetim_obj
        bolum_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
        print("form init içinden bölüm objesi seçilenler", bolum_obj)
        self.fields['bolum'].queryset = bolum_obj

    def clean(self):
        cleaned_data = super(IkiliSecForm, self).clean()
        cc_denetim = cleaned_data.get("denetim")
        cc_bolum = cleaned_data.get("bolum")
        print("denetim...:", cc_denetim)
        print( "bölum....", cc_bolum)

        if ((cc_denetim == None ) or (cc_bolum==None)):
            raise forms.ValidationError(
                    " eksik veri var.... ")

# rapor yazıları için kullanılan form
class YaziForm(forms.Form):
    denetim = forms.ModelChoiceField(queryset=denetim.objects.all(), label="Denetim Seçiniz")
    yazi = forms.CharField(label='Rapor Yazısı', widget=forms.Textarea(attrs={'cols': 80, 'rows': 40}),)
    def __init__(self, *args, **kwargs):
        kullanan = kwargs.pop("kullanan")
        super(YaziForm, self).__init__(*args, **kwargs)
        denetim_obj_ilk = denetim.objects.filter(durum="B")
        denetim_obj = denetim_obj_ilk.filter(denetci=kullanan)
        ex_list = []
        for x in denetim_obj:
            tamam_mi = True
            bolumler = sonuc_bolum.objects.filter(denetim=x.id)
            for y in bolumler:
                print("işte y...", y, "işte tamam mı...", y.tamam)
                if y.tamam == "H":
                    tamam_mi =  False
            if not tamam_mi:
                print("tamam mı hayır oldu   siliyor mu....", x)
                ex_list.append(x.id)
        print(" denetim ex list...", ex_list)
        print("denetim ilk obje................", denetim_obj)
        denetim_son_obj = denetim_obj.exclude(id__in=ex_list)
        print("denetim son obje................", denetim_son_obj)
        self.fields['denetim'].queryset = denetim_son_obj
        print("queryset initial içinden..:", self.fields['denetim'].queryset)








# ilk bölümde denetim oluşturuken kullanılan form....
class IlkDenetimSecForm(forms.Form):
    denetim_no = forms.ModelChoiceField(queryset=denetim.objects.all(), label="Denetim Seçiniz..")
    def __init__(self, *args, **kwargs):
        kullanan = kwargs.pop("kullanan")
        durum = kwargs.pop("durum")
        print("init içinden durum...", durum)
        super(IlkDenetimSecForm, self).__init__(*args, **kwargs)
        print("form init içinden kullanan", kullanan)
        denetim_obj_ilk = denetim.objects.filter(durum=durum)
        denetim_obj = denetim_obj_ilk.filter(yaratan=kullanan)
        #denetim_obj_ilk = denetim.objects.filter(durum=durum)
        print("form init içinden denetim objesi seçilenler", denetim_obj)
        self.fields['denetim_no'].queryset = denetim_obj



# ikinci kısımda canlı denetimde kullanılan form, denetçi kontrollerini yapıyor....

class DenetimSecForm(forms.Form):
    denetim_no = forms.ModelChoiceField(queryset=denetim.objects.all(), label="Denetim Seçiniz..")

    def __init__(self, *args, **kwargs):
        denetci = kwargs.pop("denetci")
        super(DenetimSecForm, self).__init__(*args, **kwargs)
        denetim_obj_ilk = denetim.objects.filter(durum="B") |  denetim.objects.filter(durum="C")
        denetim_obj = denetim_obj_ilk.filter(denetci=denetci)
        self.fields['denetim_no'].queryset = denetim_obj
        print("queryset initial içinden..:", self.fields['denetim_no'].queryset)


class DuzenleDenetimSecForm(forms.Form):
    denetim_no = forms.ModelChoiceField(queryset=denetim.objects.all(), label="Denetim Seçiniz..")

    def __init__(self, *args, **kwargs):
        denetci = kwargs.pop("denetci")
        super(DuzenleDenetimSecForm, self).__init__(*args, **kwargs)
        #denetim_obj_ilk = denetim.objects.filter(durum="B") |  denetim.objects.filter(durum="C")
        denetim_obj_ilk = denetim.objects.filter(durum="B") |  denetim.objects.filter(durum="C")
        denetim_obj = denetim_obj_ilk.filter(denetci=denetci)
        ex_list = []
        for x in denetim_obj:
            tamam_mi = True
            bolumler = sonuc_bolum.objects.filter(denetim=x.id)
            for y in bolumler:
                print("işte y...", y, "işte tamam mı...", y.tamam)
                if y.tamam == "H":
                    tamam_mi =  False
            if not tamam_mi:
                print("tamam mı hayır oldu   siliyor mu....", x)
                ex_list.append(x.id)
        print(" denetim ex list...", ex_list)
        print("denetim ilk obje................", denetim_obj)
        denetim_son_obj = denetim_obj.exclude(id__in=ex_list)
        print("denetim son obje................", denetim_son_obj)
        self.fields['denetim_no'].queryset = denetim_son_obj
        print("queryset initial içinden..:", self.fields['denetim_no'].queryset)



# ikinci kısımda canlı denetimde kullanılan form
class AcilDenetimSecForm(forms.Form):
    denetim_no = forms.ModelChoiceField(queryset=denetim.objects.all(), label="Denetim Seçiniz..")

    def __init__(self, *args, **kwargs):
        denetci = kwargs.pop("denetci")
        super(AcilDenetimSecForm, self).__init__(*args, **kwargs)
        denetim_obj_ilk = denetim.objects.filter(durum="C")
        denetim_obj = denetim_obj_ilk.filter(denetci=denetci)
        self.fields['denetim_no'].queryset = denetim_obj
        print("queryset initial içinden..:", self.fields['denetim_no'].queryset)




class BolumSecForm(forms.Form):
    bolum = forms.ModelChoiceField(queryset=sonuc_bolum.objects.all(), label="Bölüm Seçiniz..")

    def __init__(self, *args, **kwargs):
        denetim_no = kwargs.pop("denetim_no")
        devam_tekrar = kwargs.pop("devam_tekrar")
        #denetim_no = request.session    gizli = forms.CharField(required=False, initial=None)
        print("initial içinden denetim_no", denetim_no)
        super(BolumSecForm, self).__init__(*args, **kwargs)
        if devam_tekrar == "devam":
            self.fields['bolum'].queryset = sonuc_bolum.objects.filter(denetim=denetim_no).filter(tamam="H")
        else:
            self.fields['bolum'].queryset = sonuc_bolum.objects.filter(denetim=denetim_no).filter(tamam="E")
        print("queryset initial içinden..:", self.fields['bolum'].queryset)



class Sirket_Proje_Form(forms.Form):
    sirket = forms.ModelChoiceField(queryset=sirket.objects.all(),
         widget=autocomplete.ModelSelect2(url='sirket-autocomplete'), required=False)
    proje = forms.ModelChoiceField(queryset=proje.objects.all(),
         widget=autocomplete.ModelSelect2(url='sirketproje-autocomplete', forward=['sirket']  ), required=False)

    @property
    def media(self):
        m_css = {"screen": ('admin/css/vendor/select2/select2.css',
                            'admin/css/autocomplete.css',
                            'autocomplete_light/select2.css',)
                            }
        m_js = [
            #'admin/js/vendor/jquery/jquery.js',
            'autocomplete_light/jquery.init.js',
            'admin/js/vendor/select2/select2.full.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/vendor/select2/dist/js/i18n/ru.js',
            'autocomplete_light/jquery.post-setup.js',
        ]
        return forms.Media(css = m_css, js = m_js)


class NebuForm(forms.Form):
    nedirbu = forms.ModelChoiceField(queryset=denetim.objects.all(), label="nedir bu")
    def clean(self):
        cleaned_data = super(NebuForm, self).clean()
        cc_nebu = cleaned_data.get("nedirbu")
        print("ne bu...:", cc_nebu)




class KullaniciForm(forms.Form):
    pk_no = forms.IntegerField(required=False, widget=forms.HiddenInput())
    kullanici_adi = forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '20'}),label = _lazy("User Id"), localize=True,  required=False)
    adi = forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '30'}), label = _lazy("User Name"), localize=True, required=False)
    soyadi = forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '30'}), label =_lazy("User Surname"), localize=True, required=False)
    #eposta = forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '30'}), required=False)
    eposta = forms.EmailField(label = _lazy("Email address"),
                              error_messages = {'required' : _lazy("Please enter address."),
                                                'invalid'  : _lazy("Malformed address. Please correct."),})
    sirket = forms.ModelChoiceField(queryset=sirket.objects.all(), label = _lazy("Company"), localize=True, required=False)
    proje = forms.ModelChoiceField(queryset=proje.objects.all(), label = _lazy("Project"), localize=True, required=False)
    denetci = forms.ChoiceField(choices=EVETHAYIR, widget=forms.Select, localize=True, label = _lazy("Auditor"), initial="H")
    dgy = forms.ChoiceField(choices=EVETHAYIR, widget=forms.Select, localize=True, label = _lazy("Audit Supervisor"), initial="H")
    opr_alan_sefi = forms.ChoiceField(choices=EVETHAYIR, widget=forms.Select, localize=True, label = _lazy("Project Area Head"), initial="H")
    opr_teknik = forms.ChoiceField(choices=EVETHAYIR, widget=forms.Select, localize=True, label = _lazy("Project Technical Manager"), initial="H")
    opr_proje_yon = forms.ChoiceField(choices=EVETHAYIR, widget=forms.Select, localize=True, label = _lazy("Project Manager"), initial="H")
    opr_merkez_yon = forms.ChoiceField(choices=EVETHAYIR, widget=forms.Select, localize=True, label = _lazy("Projects Central Manager"), initial="H")
    isletme_projeyon = forms.ChoiceField(choices=EVETHAYIR, widget=forms.Select, localize=True, label = _lazy("Employer Project Manager"), initial="H")
    passwd_1 = forms.CharField(widget=forms.PasswordInput, required=False, localize=True, label = _lazy("Password"))
    passwd_2 = forms.CharField(widget=forms.PasswordInput, required=False, localize=True, label = _lazy("Password repeat"))


    def __init__(self, *args, **kwargs):
        sirket_adi = kwargs.pop("sirket_adi")
        print("gelen şirket  ...", sirket_adi)
        super(KullaniciForm, self).__init__(*args, **kwargs)
        sirket_obj = sirket.objects.filter(sirket_adi=sirket_adi)
        self.fields['sirket'].queryset = sirket_obj
        qs = proje.objects.filter(sirket=sirket_adi)
        print("init içinden seçilen proje listesi", qs)
        self.fields['proje'].queryset = qs
        #self.fields['eposta'].help_texts = " <br> abc@xyz.com   şeklinde girin </br>"

    def clean(self):
        cleaned_data = super(KullaniciForm, self).clean()
        cc_kullanici_adi = cleaned_data.get("kullanici_adi")
        cc_adi = cleaned_data.get("adi")
        cc_soyadi = cleaned_data.get("soyadi")
        cc_eposta = cleaned_data.get("eposta")
        cc_proje = cleaned_data.get("proje")
        cc_sirket = cleaned_data.get("sirket")
        cc_denetci = cleaned_data.get("denetci")
        cc_dgy = cleaned_data.get("dgy")
        cc_opr_alan_sefi = cleaned_data.get("opr_alan_sefi")
        cc_opr_teknik = cleaned_data.get("cc_opr_teknik")
        cc_opr_proje_yon = cleaned_data.get("opr_proje_yon")
        cc_opr_merkez_yon = cleaned_data.get("opr_merkez_yon")
        cc_isletme_projeyon = cleaned_data.get("isletme_projeyon")
        cc_passwd_1 = cleaned_data.get("passwd_1")
        cc_passwd_2 = cleaned_data.get("passwd_2")
        print("cc kullanici adı...:", cc_kullanici_adi)
        print("cc adı...:", cc_adi)
        print("cc soyadı...:", cc_soyadi)
        print("cc eposta...:", cc_eposta)
        print("cc sirket", cc_sirket)
        print("cc proje", cc_proje)
        print("cc denetçi...:", cc_denetci)
        print("cc dgy", cc_dgy)
        print("cc opr alan şefi", cc_opr_alan_sefi)
        print("cc opr teknik...:", cc_opr_teknik)
        print("cc opr proje yön ", cc_opr_proje_yon)
        print("cc opr merkez yon ", cc_opr_merkez_yon)
        print("cc işletme proje yön", cc_isletme_projeyon)
        print("cc passw 1", cc_passwd_1)
        print("cc passw 2", cc_passwd_2)

        user_obj = User.objects.filter(username=cc_kullanici_adi)
        if user_obj:
            raise forms.ValidationError(_("this username is used before!"))
        user_obj = User.objects.filter(email=cc_eposta)
        if user_obj:
            raise forms.ValidationError(_("this email is used before!"))
        if validate_password(cc_passwd_1) is not None:
            raise forms.ValidationError(_(password_validators_help_texts()), code='pw_invalid')

        return self.cleaned_data


class KullaniciSecForm(forms.Form):
    kullanici = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label="Kullanıcı",
                 widget=autocomplete.ModelSelect2Multiple(url='user-sec-autocomplete'), required=False)

    @property
    def media(self):
        m_css = {"screen": ('admin/css/vendor/select2/select2.css',
                            'admin/css/autocomplete.css',
                            'autocomplete_light/select2.css',)
                            }
        m_js = [
            #'admin/js/vendor/jquery/jquery.js',
            'autocomplete_light/jquery.init.js',
            'admin/js/vendor/select2/select2.full.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/vendor/select2/dist/js/i18n/ru.js',
            'autocomplete_light/jquery.post-setup.js',
        ]
        return forms.Media(css = m_css, js = m_js)



class ProfilResimForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profil_resmi',)
        labels = {
            'profil_resmi': 'Profil Resmi',
        }




class ParolaForm(forms.Form):
    kullanici_no = forms.IntegerField(required=False, widget=forms.HiddenInput())
    passwd_1 = forms.CharField(widget=forms.PasswordInput, required=False, localize=True, label = _lazy("Password"))
    passwd_2 = forms.CharField(widget=forms.PasswordInput, required=False, localize=True, label = _lazy("Password repeat"))

    def clean(self):
        cleaned_data = super(ParolaForm, self).clean()
        cc_kullanici_no = cleaned_data.get("kullanici_no")
        cc_passwd_1 = cleaned_data.get("passwd_1")
        cc_passwd_2 = cleaned_data.get("passwd_2")
        print("cc kullanici no", cc_kullanici_no)
        print("cc passw 1", cc_passwd_1)
        print("cc passw 2", cc_passwd_2)
        user_nesne = User.objects.get(id=cc_kullanici_no)
        if validate_password(cc_passwd_1, user=user_nesne) is not None:
            raise forms.ValidationError(_(password_validators_help_texts()), code='pw_invalid')
        return self.cleaned_data



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('sirket', 'denetci', 'denetim_grup_yetkilisi')
