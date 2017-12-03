
from django import forms
from django.forms import ModelForm
from islem.models import Profile, grup, sirket, musteri, tipi, bolum, detay
from islem.models import sonuc_bolum, denetim
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User
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

PUAN = (
('A', 'Çok İyi'),
('B', 'İyi'),
('C', 'Orta'),
('D', 'Kötü'),
)




class GozlemciForm(forms.Form):
    kisi = forms.ModelMultipleChoiceField(queryset=Profile.objects.filter(denetim_takipcisi="E"), widget=forms.SelectMultiple(), required=False)


#class gozlemciForm(forms.ModelForm):
#    class Meta:
#        model = gozlemci
#        exclude = (denetim)
#        widgets = {
#            'gozlemci': SearchableSelect(model='islem.gozlemci', search_field='gozlemci')
#        }

from django import forms
from .models import sonuc

class SonucForm(forms.ModelForm):
    class Meta:
        model = sonuc
        fields = ('sayi', 'foto', )
        widgets = {
            'sayi': forms.RadioSelect,
        }





class DetayForm(forms.Form):
    puan = forms.ChoiceField(label='Seçim....:', widget=forms.RadioSelect, choices=PUAN)
    foto = forms.ImageField()
    def clean(self):
        print(" clean self detay form..................")
        cleaned_data = super(DetayForm, self).clean()
        cc_puan = cleaned_data.get("puan")
        cc_foto = cleaned_data.get("foto")
        print ("puan...önemli...:", cc_puan)
        if not cc_puan:
            raise forms.ValidationError(" puan seçili değil.... ")
        if not cc_foto:
            raise forms.ValidationError(" foto seçili değil.... ")


class DenetimSecForm(forms.Form):
    denetim_no = forms.ModelChoiceField(queryset=denetim.objects.all(), label="Denetim Seçiniz..")
    def __init__(self, *args, **kwargs):
        denetci = kwargs.pop("denetci")
        super(DenetimSecForm, self).__init__(*args, **kwargs)
        denetim_obj_ilk = denetim.objects.filter(durum="B") | denetim.objects.filter(durum="C")
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
        #denetim_no = request.session.get('denetim_no')
        print("initial içinden denetim_no", denetim_no)
        super(BolumSecForm, self).__init__(*args, **kwargs)
        self.fields['bolum'].queryset = sonuc_bolum.objects.filter(denetim=denetim_no).exclude(tamam="T")
        #self.fields['bolum'].queryset = sonuc_bolum.objects.filter(denetim=denetim_no)
        print("queryset initial içinden..:", self.fields['bolum'].queryset)




class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('denetci', 'denetim_takipcisi', 'denetim_grup_yetkilisi')
