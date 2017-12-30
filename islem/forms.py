
from django import forms
from django.forms import ModelForm
from islem.models import Profile, grup, sirket, musteri, tipi, bolum, detay
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
from .models import sonuc

PUAN = (
('A', 'Çok İyi'),
('B', 'İyi'),
('C', 'Orta'),
('D', 'Kötü'),
)




class GozlemciForm(forms.Form):
    kisi = forms.ModelMultipleChoiceField(queryset=Profile.objects.filter(denetim_takipcisi="E"), widget=forms.SelectMultiple(), required=False)

class IlkBolumForm(forms.Form):
    bolum = forms.ModelMultipleChoiceField(queryset=bolum.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)
    def __init__(self, *args, **kwargs):
        denetim_tipi = kwargs.pop("denetim_tipi")
        super(IlkBolumForm, self).__init__(*args, **kwargs)
        print("form init içinden denetim tipi", denetim_tipi)
        self.fields['bolum'].queryset = bolum.objects.filter(tipi=denetim_tipi)
        print("queryset initial içinden..:", self.fields['bolum'].queryset)

class IlkDetayForm(forms.Form):
    detay = forms.ModelMultipleChoiceField(queryset=detay.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)
    def __init__(self, *args, **kwargs):
        bolum_no = kwargs.pop("bolum_no")
        super(IlkDetayForm, self).__init__(*args, **kwargs)
        print("form init içinden bölüm no", bolum_no)
        self.fields['detay'].queryset = detay.objects.filter(bolum=bolum_no)
        print("queryset initial içinden..:", self.fields['detay'].queryset)



# esas işin döndüğü yer foto yüklüyor................
#
class SonucForm(forms.ModelForm):
    class Meta:
        model = sonuc
        fields = ('sayi', 'foto', )
        widgets = {
            'sayi': forms.RadioSelect,
            #'foto': forms.HiddenInput(),
        }


class DenetimForm(forms.ModelForm):
    class Meta:
        model = denetim
        fields = ('denetim_adi', 'musteri', 'denetci', 'tipi', 'hedef_baslangic', 'hedef_bitis', 'aciklama')
    def clean(self):
        print(" clean denetim form................")
        cleaned_data = super(DenetimForm, self).clean()
        cc_hedef_baslangic = self.cleaned_data.get("hedef_baslangic")
        cc_hedef_bitis = self.cleaned_data.get("hedef_bitis")
        print("hedef başlangıç...:", cc_hedef_baslangic)
        print("hedef_bitis", cc_hedef_bitis)
        #if ( cc_hedef_baslangic > cc_hedef_bitis ):
        #    raise ValidationError(" tarih sıralaması yanlış...")



class Denetim_BForm(forms.Form):
    denetim_adi = forms.CharField()
    musteri = forms.ModelChoiceField(label='Müşteri..:', queryset=musteri.objects.all())
    denetci = forms.ModelChoiceField(label='Denetçi..:', queryset=Profile.objects.filter(denetci="E"))
    tipi = forms.ModelChoiceField(label='Tipi..:', queryset=tipi.objects.all())
    hedef_baslangic = forms.DateField(label='Hedef başlangıç...:', widget=forms.TextInput(attrs={ 'class':'datepicker' }))
    hedef_bitis = forms.DateField(label='Hedef bitiş...:', widget=forms.TextInput(attrs={ 'class':'datepicker' }))
    aciklama = forms.CharField(label='Açıklama', widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}),)

    def clean(self):
        cleaned_data = super(Denetim_BForm, self).clean()
        cc_hedef_baslangic = cleaned_data.get("hedef_baslangic")
        cc_hedef_bitis = cleaned_data.get("hedef_bitis")
        print("hedef başlangıç...:", cc_hedef_baslangic)
        print("hedef_bitis", cc_hedef_bitis)
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
        print("bolum....", cc_bolum)

        if ((cc_denetim == None ) or (cc_bolum==None)):
            raise forms.ValidationError(
                    " eksik veri var.... ")



# ilk bölümde denetim oluşturuken kullanılan form....
class IlkDenetimSecForm(forms.Form):
    denetim_no = forms.ModelChoiceField(queryset=denetim.objects.all(), label="Denetim Seçiniz..")
    def __init__(self, *args, **kwargs):
        kullanan = kwargs.pop("kullanan")
        durum = kwargs.pop("durum")
        super(IlkDenetimSecForm, self).__init__(*args, **kwargs)
        print("form init içinden kullanan", kullanan)
        denetim_obj_ilk = denetim.objects.filter(durum=durum)
        denetim_obj = denetim_obj_ilk.filter(yaratan=kullanan)
        self.fields['denetim_no'].queryset = denetim_obj
        print("queryset initial içinden..:", self.fields['denetim_no'].queryset)


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


"""
class BolumChoiceField(django.forms.ModelChoiceField):
     queryset = sonuc_bolum.objects.all()
     def label_from_instance(self, obj):
         return obj.bolum
"""

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




class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('denetci', 'denetim_takipcisi', 'denetim_grup_yetkilisi')
