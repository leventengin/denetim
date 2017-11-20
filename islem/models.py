from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


EVETHAYIR = (
('E', 'Evet'),
('H', 'Hayır'),
)

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    denetci = models.CharField(max_length=1, choices=EVETHAYIR)
    denetim_takipcisi = models.CharField(max_length=1, choices=EVETHAYIR)
    denetim_grup_yetkilisi = models.CharField(max_length=1, choices=EVETHAYIR)
    def __str__(self):
        return(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class tipi(models.Model):
    tipi_kodu = models.CharField(max_length=10)
    tipi_adi = models.CharField(max_length=200)
    def __str__(self):
        return(self.tipi_adi)

class bolum(models.Model):
    bolum_kodu = models.CharField(max_length=10)
    bolum_adi = models.CharField(max_length=200)
    tipi = models.ForeignKey(tipi, on_delete=models.PROTECT)
    def __str__(self):
        return(self.bolum_adi)

class detay(models.Model):
    detay_kodu = models.CharField(max_length=5)
    detay_adi = models.CharField(max_length=200)
    bolum = models.ForeignKey(bolum, on_delete=models.PROTECT)
    def __str__(self):
        return(self.detay_adi)


class grup(models.Model):
    grup_adi = models.CharField(max_length=200)
    def __str__(self):
        return(self.grup_adi)


class sirket(models.Model):
    sirket_adi = models.CharField(max_length=200)
    grubu = models.ForeignKey(grup, on_delete=models.PROTECT)
    def __str__(self):
        return(self.sirket_adi)

class musteri(models.Model):
    musteri_adi = models.CharField(max_length=200)
    def __str__(self):
        return(self.musteri_adi)
