""
from django import forms
from django.forms import ModelForm
from islem.models import Profile, grup, sirket, proje, tipi, bolum, detay, acil
from islem.models import sonuc_bolum, denetim, kucukresim, zon, plan_opr_gun, yer, proje_alanlari
from webservice.models import rfid_dosyasi
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User, Group
#from __future__ import unicode_literals
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
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
#from django.core.exceptions import ValidationError
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

from django.utils.encoding import force_text

OPERASYONDIGER = (
('O', 'Operasyon'),
('D', 'Diğer'),
)


EVETHAYIR = (
('E', 'Evet'),
('H', 'Hayır'),
)

GUNLER = (
('Pzt', 'Pazartesi'),
('Sal', 'Salı'),
('Çar', 'Çarşamba'),
('Per', 'Perşembe'),
('Cum', 'Cuma'),
('Cmt', 'Cumartesi'),
('Paz', 'Pazar'),
)


RUTINPLANLI = (
('P', 'Planlı'),
('R', 'Rutin'),
('S', 'Sıralı'),
)

PUANLAMA_TURU = (
('A', 'Onluk'),
('B', 'Beşlik'),
('C', 'İkilik'),
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




class Denetim_Rutin_Baslat_Form(forms.Form):
    denetim = forms.ModelChoiceField(queryset=denetim.objects.all(),
                 widget=autocomplete.ModelSelect2(url='denetim-rutin-autocomplete'), required=False)





class Den_Olustur_Form(forms.Form):
    denetim = forms.ModelChoiceField(queryset=denetim.objects.all(),
                 widget=autocomplete.ModelSelect2(url='denolustur-autocomplete'), required=False)



class Qrcode_Form(forms.Form):
    denetim = forms.ModelChoiceField(queryset=denetim.objects.all(),
                 widget=autocomplete.ModelSelect2(url='rutindenetim-autocomplete'), required=False)
    qrcode = forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '40'}))



class Ikili_Deneme_Form(forms.Form):
    denetim_deneme = forms.ModelChoiceField(queryset=denetim.objects.all(),
         widget=autocomplete.ModelSelect2(url='denetim-autocomplete'), required=False)
    sonuc_bolum_deneme = forms.ModelChoiceField(queryset=sonuc_bolum.objects.all(),
         widget=autocomplete.ModelSelect2(url='sonucbolum-autocomplete', forward=['denetim_deneme']  ), required=False)




class ProjeSecForm(forms.Form):
    proje = forms.ModelChoiceField(queryset=proje.objects.all(),
                 widget=autocomplete.ModelSelect2(url='proje-autocomplete'), required=False)


class SoruListesiForm(forms.Form):
    tipi = forms.ModelChoiceField(queryset=tipi.objects.all(),
         widget=autocomplete.ModelSelect2(url='list_tipi-autocomplete'), required=False)
    zon = forms.ModelChoiceField(queryset=zon.objects.all(),
         widget=autocomplete.ModelSelect2(url='list_zon-autocomplete', forward=['tipi'] ), required=False)
    bolum = forms.ModelChoiceField(queryset=bolum.objects.all(),
         widget=autocomplete.ModelSelect2(url='list_bolum-autocomplete', forward=['zon'] ), required=False)


# esas işin döndüğü yer foto yüklüyor................
#
class SonucForm(forms.ModelForm):
    class Meta:
        model = sonuc_detay
        fields = ( 'puanlama_turu', 'onluk', 'beslik', 'ikilik', 'denetim_disi', 'resim_varmi',)
        widgets = {
            'resim_varmi' : forms.HiddenInput(),
        }
        labels = {
            'denetim_disi' : "Denetim dışı",
            'onluk' : "Puan",
            'beslik': "Puan",
            'ikilik': "Puan",
        }
    def __init__(self, *args, **kwargs):
        puanlama_turu = kwargs.pop("puanlama_turu")
        super(SonucForm, self).__init__(*args, **kwargs)
        print("puanlama türü initial içinden..:", puanlama_turu)
        self.fields['puanlama_turu'].value = puanlama_turu
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
        cc_resim_varmi = cleaned_data.get("resim_varmi")
        print("cc puanlama türü...:", cc_puanlama_turu)
        print("cc onluk", cc_onluk)
        print("cc beslik", cc_beslik)
        print("cc ikilik", cc_ikilik)
        print("cc denetim dışı", cc_denetim_disi)
        print("cc resim var mı", cc_resim_varmi)



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

class GunForm(forms.Form):
    gun = forms.ChoiceField(choices=GUNLER, widget=forms.Select, label="Gün Seçiniz:")

#class SaatForm(forms.Form):
#    saat = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

class SaatForm(forms.ModelForm):
    class Meta:
        model = plan_opr_gun
        fields = ( 'zaman',)
        labels = {
            'zaman' : "Saat giriniz:",
        }
    def clean(self):
        cleaned_data = super(SaatForm, self).clean()
        cc_zaman = cleaned_data.get("zaman")
        print("cc zaman", cc_zaman)




class YerForm(forms.ModelForm):
    class Meta:
        model = yer
        fields = ( 'proje_alanlari', 'yer_adi', 'mac_no', 'opr_basl', 'opr_son', 'opr_delta', 'den_basl', 'den_son', 'den_delta')
        labels = {
            'proje_alanlari' : 'Proje Alanı:',
            'yer_adi' : 'Yer Adı:',
            'mac_no': 'Mac No:',
            'opr_basl': 'Opr Başlangıç:',
            'opr_son': 'Opr Son:',
            'opr_delta': 'Opr Aralık',
            'den_basl': 'Den Başlangıç:',
            'den_son': 'Den Son:',
            'den_delta': 'Den Aralık',
        }

    def clean(self):
        cleaned_data = super(YerForm, self).clean()
        cc_pa = cleaned_data.get("proje_alanlari")
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




class RfidForm(forms.ModelForm):
    class Meta:
        model = rfid_dosyasi
        fields = ( 'rfid_no', 'proje', 'rfid_tipi', 'calisan', 'adi', 'soyadi')
        labels = {
            'rfid_no': 'RFID No',
            'proje' : 'Proje Adı:',
            'rfid_tipi' : 'RFID Tipi:',
            'çalışan': 'Kullanıcı:',
            'adi' : 'Adı:',
            'soyadi' : 'Soyadı:',
        }

    def __init__(self, *args, **kwargs):
        kullanici = kwargs.pop("kullanici")
        super(RfidForm, self).__init__(*args, **kwargs)
        prj = kullanici.profile.proje
        print("işte yer form init içinden proje...", prj)
        proje_obj = proje.objects.filter(id=prj.id)
        print("işte  proje objesi.....", proje_obj)
        self.fields['proje'].queryset = proje_obj

    def clean(self):
        cleaned_data = super(RfidForm, self).clean()
        rfid_no = cleaned_data.get('rfid_no')
        proje = cleaned_data.get('proje')
        rfid_tipi = cleaned_data.get('rfid_tipi')
        calisan = cleaned_data.get('calisan')
        adi = cleaned_data.get('adi')
        soyadi = cleaned_data.get('soyadi')

        print("cc rfid no", rfid_no)
        print("cc proje", proje)
        print("cc rfid tipi", rfid_tipi)
        print("cc çalışan", calisan)
        print("cc adi", adi)
        print("cc soyadi", soyadi)

        if (rfid_tipi == "O") and (adi == ""):
            print(" ne oluyor burada....")
            raise forms.ValidationError("isim alanı boş olamaz.... ")

        if (rfid_tipi == "O") and (adi == ""  or  soyadi == ""):
            print(" ne oluyor burada....")
            raise forms.ValidationError("soyad alanı boş olamaz.... ")

        if (rfid_tipi == "D") and (calisan == None):
            print("yoksa burada.........")
            raise forms.ValidationError("kullanıcı alanı boş olamaz...")

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
            """
            if (cc_hedef_baslangic.date < datetime.today()):
                raise forms.ValidationError(
                        " denetim başlangıcı için ileri bir tarih girmelisiniz.... ")
            if (cc_hedef_bitis < datetime.date.today()):
                raise forms.ValidationError(
                        " denetim bitişi için ileri bir tarih girmelisiniz.... ")
            """
        return self.cleaned_data


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
        #kullanan = request.user.id
        super(YaziForm, self).__init__(*args, **kwargs)
        print("form init içinden kullanan", kullanan)
        denetim_obj_ilk = denetim.objects.filter(durum="C")
        denetim_obj = denetim_obj_ilk.filter(yaratan=kullanan)
        self.fields['denetim'].queryset = denetim_obj


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



class NebuForm(forms.Form):
    nedirbu = forms.ModelChoiceField(queryset=denetim.objects.all(), label="nedir bu")
    def clean(self):
        cleaned_data = super(NebuForm, self).clean()
        cc_nebu = cleaned_data.get("nedirbu")
        print("ne bu...:", cc_nebu)





class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('sirket', 'denetci', 'denetim_grup_yetkilisi')
