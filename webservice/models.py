from django.conf import settings
from django.db import models
from django.urls import reverse
from islem.models import proje_alanlari, yer, proje
from rest_framework.reverse import reverse as api_reverse

import datetime
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests


# django hosts --> subdomain for reverse

class BlogPost(models.Model):
    # pk aka id --> numbers
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title       = models.CharField(max_length=120, null=True, blank=True)
    content     = models.TextField(max_length=120, null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)

    @property
    def owner(self):
        return self.user
    # def get_absolute_url(self):
    #     return reverse("api-postings:post-rud", kwargs={'pk': self.pk}) '/api/postings/1/'

    def get_api_url(self, request=None):
        return api_reverse("api-ws:post-rud", kwargs={'pk': self.pk}, request=request)


class MacPost(models.Model):
    # pk aka id --> numbers
    mac_no      = models.CharField(max_length=20)
    timestamp   = models.DateTimeField()

    def __str__(self):
        return str(self.mac_no)

    @property
    def owner(self):
        return self.mac_no


    def get_api_url(self, request=None):
        return api_reverse("api-ws:mac-rud", kwargs={'pk': self.pk}, request=request)



class Memnuniyet(models.Model):
    mac_no      = models.CharField(max_length=20)
    tipi        = models.CharField(max_length=2)
    oy          = models.CharField(max_length=1)
    sebep       = models.CharField(max_length=2)
    gelen_tarih = models.CharField(max_length=30)
    timestamp   = models.DateTimeField()

    def __str__(self):
        return str(self.mac_no)

    @property
    def owner(self):
        return self.mac_no

    def get_api_url(self, request=None):
        return api_reverse("api-ws:memnuniyet-rud", kwargs={'pk': self.pk}, request=request)


class Operasyon_Data(models.Model):
    mac_no      = models.CharField(max_length=20)
    tipi        = models.CharField(max_length=2)
    rfid_no     = models.CharField(max_length=20)
    bas_tarih   = models.CharField(max_length=30)
    son_tarih   = models.CharField(max_length=30)
    bild_tipi   = models.CharField(max_length=1)
    timestamp   = models.DateTimeField()

    def __str__(self):
        return str(self.mac_no)

    @property
    def owner(self):
        return self.mac_no

    def get_api_url(self, request=None):
        return api_reverse("api-ws:operasyon-rud", kwargs={'pk': self.pk}, request=request)

class Denetim_Data(models.Model):
    mac_no      = models.CharField(max_length=20)
    tipi        = models.CharField(max_length=2)
    rfid_no     = models.CharField(max_length=20)
    kod         = models.CharField(max_length=8)
    gelen_tarih = models.CharField(max_length=30)
    timestamp   = models.DateTimeField()

    def __str__(self):
        return str(self.mac_no)

    @property
    def owner(self):
        return self.mac_no

    def get_api_url(self, request=None):
        return api_reverse("api-ws:denetim-rud", kwargs={'pk': self.pk}, request=request)

class Ariza_Data(models.Model):
    mac_no      = models.CharField(max_length=20)
    tipi        = models.CharField(max_length=2)
    rfid_no     = models.CharField(max_length=20)
    sebep       = models.CharField(max_length=2)
    gelen_tarih = models.CharField(max_length=30)
    timestamp   = models.DateTimeField()

    def __str__(self):
        return str(self.mac_no)

    @property
    def owner(self):
        return self.mac_no

    def get_api_url(self, request=None):
        return api_reverse("api-ws:ariza-rud", kwargs={'pk': self.pk}, request=request)



OPERASYONDIGER = (
('O', 'Operasyon'),
('D', 'Diğer'),
)



class rfid_dosyasi(models.Model):
    rfid_no = models.CharField(max_length=20)
    proje = models.ForeignKey('islem.proje', on_delete=models.PROTECT)
    rfid_tipi = models.CharField(max_length=1, choices=OPERASYONDIGER)
    calisan = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    adi = models.CharField(max_length=20, null=True, blank=True)
    soyadi = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return '%s-%s' % (self.rfid_no, self.proje)

    @property
    def owner(self):
        return self.rfid_no

    def get_api_url(self, request=None):
        return api_reverse("api-ws:rfid-rud", kwargs={'pk': self.pk}, request=request)



@receiver(post_save, sender=rfid_dosyasi)
def create_rfid_yeni(sender, instance, **kwargs):
    print("receiver post save rfid...............")
    proje = instance.proje
    print(" receiver post save proje.............", proje)
    alan_obj = proje_alanlari.objects.filter(proje=proje)
    print("projedeki alanlar....", alan_obj)

    for alan in alan_obj:
        yer_obj = yer.objects.filter(proje_alanlari=alan)
        for deger in yer_obj:
            yer_updown_obj = yer_updown.objects.filter(mac_no=deger.mac_no).first()
            if yer_updown_obj:
                mac_no = deger.mac_no
                kaydetme_obj = yer_updown(id=yer_updown_obj.id,
                                          proje=proje,
                                          mac_no=mac_no,
                                          degis="E")
                kaydetme_obj.save()
            else:
                mac_no = deger.mac_no
                kaydetme_obj = yer_updown(proje=proje,
                                          mac_no=mac_no,
                                          degis="E")
                kaydetme_obj.save()



@receiver(post_save, sender=yer)
def create_yerupdown_yeni(sender, instance, **kwargs):
    print("receiver post save rfid...............")
    yer_id = instance.id
    yer_obj = yer.objects.get(id=yer_id)
    proje_alani = yer_obj.proje_alanlari.id
    print("proje alanı...", proje_alani)
    proje = proje_alanlari.objects.get(id=proje_alani).proje.id
    mac_no_x = instance.mac_no

    yer_updown_obj = yer_updown.objects.filter(mac_no=mac_no_x).first()
    if yer_updown_obj:
        kaydetme_obj = yer_updown(id=yer_updown_obj.id,
                                  proje_id=proje,
                                  mac_no=mac_no_x,
                                  degis="E")
        kaydetme_obj.save()
    else:
        kaydetme_obj = yer_updown(proje_id=proje,
                                  mac_no=mac_no_x,
                                  degis="E")
        kaydetme_obj.save()



EVETHAYIR = (
('E', 'Evet'),
('H', 'Hayır'),
)


class yer_updown(models.Model):
    mac_no = models.CharField(max_length=20)
    proje = models.ForeignKey('islem.proje', on_delete=models.PROTECT)
    degis = models.CharField(max_length=1, choices=EVETHAYIR, default="E")
    alive_time = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return '%s-%s' % (self.mac_no, self.proje)

    @property
    def owner(self):
        return self.yer

    def get_api_url(self, request=None):
        return api_reverse("api-ws:yerud-rud", kwargs={'pk': self.pk}, request=request)
