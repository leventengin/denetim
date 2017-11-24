
from django import forms
from django.forms import ModelForm
from islem.models import Profile, grup, sirket, musteri, tipi, bolum, detay
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User
#from __future__ import unicode_literals
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from bootstrap_datepicker.widgets import DatePicker
import datetime
from datetime import date

from django.core import serializers
from django.contrib.postgres.search import SearchVector
from django.views.generic import FormView
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from datetime import date, datetime
from django.template.loader import render_to_string
import requests






class GozlemciForm(forms.Form):
    kisi = forms.ModelMultipleChoiceField(queryset=Profile.objects.filter(denetim_takipcisi="E"), widget=forms.SelectMultiple(), required=False)


#class gozlemciForm(forms.ModelForm):
#    class Meta:
#        model = gozlemci
#        exclude = (denetim)
#        widgets = {
#            'gozlemci': SearchableSelect(model='islem.gozlemci', search_field='gozlemci')
#        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('denetci', 'denetim_takipcisi', 'denetim_grup_yetkilisi')
