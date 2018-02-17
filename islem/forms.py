
from django import forms
from django.forms import ModelForm
from islem.models import Profile, grup, sirket, proje, tipi, bolum, detay, acil
from islem.models import sonuc_bolum, denetim, kucukresim
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
from django.core.exceptions import ValidationError
from django import forms
from .models import sonuc_detay
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







PUAN = (
('A', 'Çok İyi'),
('B', 'İyi'),
('C', 'Orta'),
('D', 'Kötü'),
)



class Denetim_Deneme_Form(forms.Form):
    denetim = forms.ModelChoiceField(queryset=denetim.objects.all(),
                 widget=autocomplete.ModelSelect2(url='denetim-autocomplete'), required=False)

    def clean(self):
        cleaned_data = super(Denetim_Deneme_Form, self).clean()
        cc_denetim = cleaned_data.get("denetim")
        print("cc denetim ..:", cc_denetim)




class Ikili_Deneme_Form(forms.Form):
    denetim_deneme = forms.ModelChoiceField(queryset=denetim.objects.all(),
         widget=autocomplete.ModelSelect2(url='denetim-autocomplete'), required=False)
    sonuc_bolum_deneme = forms.ModelChoiceField(queryset=sonuc_bolum.objects.all(),
         widget=autocomplete.ModelSelect2(url='sonucbolum-autocomplete', forward=['denetim_deneme']  ), required=False)



# esas işin döndüğü yer foto yüklüyor................
#
class SonucForm(forms.ModelForm):
    class Meta:
        model = sonuc_detay
        fields = ('sayi', 'foto', )
        widgets = {
            'sayi': forms.RadioSelect,
            #'foto': forms.HiddenInput(),
        }




class AcilAcForm(forms.Form):
    denetim = forms.ModelChoiceField(queryset=denetim.objects.all(), label="Denetim Seçiniz..")
    konu = forms.CharField()
    aciklama = forms.CharField(label='Açıklama', widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}),)
    def __init__(self, *args, **kwargs):
        denetci = kwargs.pop("denetci")
        super(AcilAcForm, self).__init__(*args, **kwargs)
        denetim_obj_ilk = denetim.objects.filter(durum="C")
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



class Denetim_BForm(forms.Form):
    denetim_adi = forms.CharField()
    proje = forms.ModelChoiceField(label='Proje..:', queryset=proje.objects.all())
    denetci = forms.ModelChoiceField(label='Denetçi..:', queryset=Profile.objects.filter(denetci="E"))
    tipi = forms.ModelChoiceField(label='Tipi..:', queryset=tipi.objects.all())
    gozlemci_many = forms.ModelChoiceField(queryset=User.objects.all(),
                 widget=autocomplete.ModelSelect2Multiple(url='takipci-autocomplete'), required=False)
    hedef_baslangic = forms.DateField(label='Hedef başlangıç...:', widget=forms.TextInput(attrs={ 'class':'datepicker' }))
    hedef_bitis = forms.DateField(label='Hedef bitiş...:', widget=forms.TextInput(attrs={ 'class':'datepicker' }))
    aciklama = forms.CharField(label='Açıklama', widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}),)



class DenetimForm(forms.Form):
    pk_no = forms.IntegerField(required=False, widget=forms.HiddenInput())
    denetim_adi = forms.CharField(widget=forms.TextInput(attrs={'class':'special', 'size': '50'}))
    proje = forms.ModelChoiceField(queryset=proje.objects.all(),
                     widget=autocomplete.ModelSelect2(url='proje-autocomplete'), required=False)
    denetci = forms.ModelChoiceField(queryset=Profile.objects.filter(denetci="E"),
                     widget=autocomplete.ModelSelect2(url='denetci-autocomplete'), required=False)
    tipi = forms.ModelChoiceField(queryset=tipi.objects.all(),
                 widget=autocomplete.ModelSelect2(url='tipi-autocomplete'), required=False)
    takipciler = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label='Takipçiler',
                widget=autocomplete.ModelSelect2Multiple(url='takipci-autocomplete'), required=False)
    hedef_baslangic = forms.DateField(label='Hedef başlangıç...:',
                        widget=forms.TextInput(attrs={ 'class':'datepicker' }))
    hedef_bitis = forms.DateField(label='Hedef bitiş...:',
                        widget=forms.TextInput(attrs={ 'class':'datepicker' }))
    aciklama = forms.CharField(label='Açıklama', widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}),)
    bolum = forms.ModelMultipleChoiceField(queryset=bolum.objects.all(), label='Bölümler...............:',
                 widget=autocomplete.ModelSelect2Multiple(url='bolum-autocomplete', forward=['tipi'] ), required=False)
    detay = forms.ModelMultipleChoiceField(queryset=detay.objects.all(), label=None,
            widget=forms.CheckboxSelectMultiple(attrs={"checked":""}), required=False)

    def __init__(self, *args, **kwargs):
        bolum_listesi = kwargs.pop("bolum_listesi")
        init_param = kwargs.pop("init_param")
        super(DenetimForm, self).__init__(*args, **kwargs)
        print("init içinden seçilen bölüm listesi", bolum_listesi)
        print("init param...", init_param)
        if init_param:
            qs = detay.objects.none()
            if not (bolum_listesi == None):
                i = 0
                print("len...", len(bolum_listesi))
                while i < len(bolum_listesi):
                    qx = detay.objects.filter(bolum=bolum_listesi[i])
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
        print("cc denetçi...:", cc_denetci)
        print("cc tipi", cc_tipi)
        print("cc takipçiler", cc_takipciler)
        print("cc hedef başlangıç...:", cc_hedef_baslangic)
        print("cc hedef_bitis", cc_hedef_bitis)
        print("cc açıklama ", cc_aciklama)
        print("cc bolum", cc_bolum)
        print("cc detay", cc_detay)
        #if cc_hedef_baslangic == None:
        #     raise forms.ValidationError(
        #          " denetim başlangıç tarihi girmelisiniz.... ")

        if (cc_hedef_baslangic != None ) and (cc_hedef_baslangic < date.today()):
            raise forms.ValidationError(
                    " denetim başlangıcı için ileri bir tarih girmelisiniz.... ")
        #if cc_hedef_bitis == None:
        #    raise forms.ValidationError(
        #            " denetim bitiş tarihi girmelisiniz.... ")
        if (cc_hedef_bitis != None ) and (cc_hedef_bitis < date.today()):
            raise forms.ValidationError(
                    " denetim bitişi için ileri bir tarih girmelisiniz.... ")
        if (cc_hedef_baslangic != None ) and (cc_hedef_bitis != None ) and (cc_hedef_baslangic > cc_hedef_bitis):
            raise forms.ValidationError(" tarih sıralaması yanlış...")



# ilk bölümde denetimin bölümleri seçilirken kullanılan form...
class IlkBolumForm(forms.Form):
    bolum = forms.ModelMultipleChoiceField(queryset=bolum.objects.all(), label='Bölümler...............:',
                 widget=autocomplete.ModelSelect2Multiple(url='bolum-autocomplete', forward=['tipi'] ), required=False)
    def clean(self):
        cleaned_data = super(IlkBolumForm, self).clean()
        cc_bolum = cleaned_data.get("bolum")
        print(" bölümler..", cc_bolum)

class IlkDetayForm(forms.Form):
    detay = forms.ModelMultipleChoiceField(queryset=detay.objects.all(), label="",
            widget=forms.CheckboxSelectMultiple(attrs={"checked":""}), required=False)
    def clean(self):
        cleaned_data = super(IlkDetayForm, self).clean()
        cc_detay = cleaned_data.get("detay")
        print("detaylar..", cc_detay)
    def __init__(self, *args, **kwargs):
        bolum_listesi = kwargs.pop("bolum_listesi")
        super(IlkDetayForm, self).__init__(*args, **kwargs)
        print("init içinden seçilen bölüm listesi", bolum_listesi)
        qs = detay.objects.none()
        if not (bolum_listesi == None):
            i = 0
            print("len...", len(bolum_listesi))
            while i < len(bolum_listesi):
                qx = detay.objects.filter(bolum=bolum_listesi[i])
                print("qx...", qx)
                qs = qs.union(qx)
                i = i+1
        qs = qs.order_by('detay_kodu')
        print("qs.....", qs)
        self.fields['detay'].queryset = qs


class YeniTarihForm(forms.Form):
    hedef_baslangic = forms.DateField(label='Hedef başlangıç...:', widget=forms.TextInput(attrs={ 'class':'datepicker' }))
    hedef_bitis = forms.DateField(label='Hedef bitiş...:', widget=forms.TextInput(attrs={ 'class':'datepicker' }))
    def clean(self):
        cleaned_data = super(YeniTarihForm, self).clean()
        cc_hedef_baslangic = cleaned_data.get("hedef_baslangic")
        cc_hedef_bitis = cleaned_data.get("hedef_bitis")
        print("hedef başlangıç...:", cc_hedef_baslangic)
        print("hedef_bitis", cc_hedef_bitis)
        if (cc_hedef_baslangic != None ) and (cc_hedef_baslangic < date.today()):
            raise forms.ValidationError(
                    " denetim başlangıcı için ileri bir tarih girmelisiniz.... ")
        if (cc_hedef_bitis != None ) and (cc_hedef_bitis < date.today()):
            raise forms.ValidationError(
                    " denetim bitişi için ileri bir tarih girmelisiniz.... ")
        if (cc_hedef_baslangic != None ) and (cc_hedef_bitis != None ) and (cc_hedef_baslangic > cc_hedef_bitis):
            raise forms.ValidationError(" tarih sıralaması yanlış...")


class KucukResimForm(forms.ModelForm):
    class Meta:
        model = kucukresim
        fields = ('foto_kucuk',)


# artık anlamı yok modelform olan sonucform çalışıyor...........
class DetayForm(forms.Form):
    puan = forms.ChoiceField(label='Seçim....:', widget=forms.RadioSelect, choices=PUAN)
    foto = forms.ImageField()
    def clean(self):
        print(" clean self detay form..................")
        cleaned_data = super(DetayForm, self).clean()
        cc_puan = self.cleaned_data.get("puan")
        image_file = self.cleaned_data.get("foto")
        print ("puan...önemli...:", cc_puan)

        if not cc_puan:
            raise forms.ValidationError(" puan seçili değil.... ")

        if not image_file:
            raise forms.ValidationError(" foto seçili değil.... ")

        if not image_file.name.endswith(".jpg"):
            raise forms.ValidationError("  Sadece .jpg yüklenmektedir")


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



# ilk bölümde denetim oluşturuken kullanılan form....
class IlkDenetimSecForm(forms.Form):
    denetim_no = forms.ModelChoiceField(queryset=denetim.objects.all(), label="Denetim Seçiniz..")
    def __init__(self, *args, **kwargs):
        kullanan = kwargs.pop("kullanan")
        durum = kwargs.pop("durum")
        print("init içinden durum...", durum)
        super(IlkDenetimSecForm, self).__init__(*args, **kwargs)
        print("form init içinden kullanan", kullanan)
        #denetim_obj_ilk = denetim.objects.filter(durum=durum)


# ikinci kısımda canlı denetimde kullanılan form
class DenetimSecForm(forms.Form):
    denetim_no = forms.ModelChoiceField(queryset=denetim.objects.all(), label="Denetim Seçiniz..")
    def __init__(self, *args, **kwargs):
        denetci = kwargs.pop("denetci")
        super(DenetimSecForm, self).__init__(*args, **kwargs)
        denetim_obj_ilk = denetim.objects.filter(durum="C") | denetim.objects.filter(durum="D")
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



# ilk kısımda denetçi değiştirirken kullanılan form
class YeniDenetciSecForm(forms.Form):
    yeni_denetci = forms.ModelChoiceField(queryset=Profile.objects.filter(denetci="E"), label="Yeni Denetçi Seçiniz..")
    def __init__(self, *args, **kwargs):
        denetci = kwargs.pop("denetci")
        super(YeniDenetciSecForm, self).__init__(*args, **kwargs)
        denetciler = Profile.objects.filter(denetci="E").exclude(user=denetci)
        self.fields['yeni_denetci'].queryset = denetciler
        print("queryset initial içinden..:", self.fields['yeni_denetci'].queryset)



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
