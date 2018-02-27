from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime, date
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from gm2m import GM2MField

EVETHAYIR = (
('E', 'Evet'),
('H', 'Hayır'),
)

ACIKKAPANDI = (
('A', 'Açık'),
('K', 'Kapandı'),
)

DENETCIPROJE = (
('D', 'Denetçi'),
('P', 'Proje'),
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


class grup(models.Model):
    grup_adi = models.CharField(max_length=200)
    def __str__(self):
        return(self.grup_adi)


class sirket(models.Model):
    sirket_adi = models.CharField(max_length=200)
    grubu = models.ForeignKey(grup, on_delete=models.PROTECT)
    turu = models.CharField(max_length=1, choices=DENETCIPROJE, default="P")
    def __str__(self):
        return(self.sirket_adi)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sirket = models.ForeignKey(sirket, on_delete=models.PROTECT, null=True, blank=True)
    denetci = models.CharField(max_length=1, choices=EVETHAYIR)
    denetim_grup_yetkilisi = models.CharField(max_length=1, choices=EVETHAYIR)
    def __str__(self):
        return(self.user.username)



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

class zon(models.Model):
    zon_kodu = models.CharField(max_length=10)
    zon_adi = models.CharField(max_length=200)
    tipi = models.ForeignKey(tipi, on_delete=models.PROTECT)
    def __str__(self):
        return '%s-%s' % (self.zon_kodu, self.zon_adi)

class bolum(models.Model):
    bolum_kodu = models.CharField(max_length=10)
    bolum_adi = models.CharField(max_length=200)
    zon = models.ForeignKey(zon, on_delete=models.PROTECT, default=1)
    def __str__(self):
        return '%s-%s' % (self.bolum_kodu, self.bolum_adi)

class detay(models.Model):
    detay_kodu = models.CharField(max_length=5)
    detay_adi = models.CharField(max_length=200)
    bolum = models.ForeignKey(bolum, on_delete=models.PROTECT)
    puanlama_turu = models.CharField(max_length=1, choices=PUANLAMA_TURU, default="A")
    def __str__(self):
        return '%s-%s' % (self.detay_kodu, self.detay_adi)
        #return(self.detay_adi)


class proje(models.Model):
    proje_adi = models.CharField(max_length=200)
    sirket = models.ForeignKey(sirket, on_delete=models.PROTECT)
    ilgililer = models.ManyToManyField(User, related_name='ilgililer')
    proje_yonetici = models.ForeignKey(User, related_name='yonetici',  on_delete=models.CASCADE)
    def __str__(self):
        return(self.proje_adi)


class denetim(models.Model):
    denetim_adi = models.CharField(max_length=100)
    proje = models.ForeignKey(proje, on_delete=models.PROTECT)
    rutin_planli = models.CharField(max_length=1, choices=RUTINPLANLI)
    r_erisim = models.IntegerField(blank=True, null=True)
    denetci = models.ForeignKey(User, related_name='denetci', on_delete=models.CASCADE, null=True)
    tipi = models.ForeignKey(tipi, on_delete=models.PROTECT)
    durum = models.CharField(max_length=1, default="A")
    yaratim_tarihi = models.DateField(_("Date"), default=datetime.today)
    yaratan = models.ForeignKey(User, related_name='yaratan', on_delete=models.CASCADE)
    hedef_baslangic = models.DateField(blank=True, null=True)
    hedef_bitis = models.DateField(blank=True, null=True)
    gerc_baslangic = models.DateField(blank=True, null=True)
    gerc_bitis = models.DateField(blank=True, null=True)
    fiili_kapanis = models.DateField(blank=True, null=True)
    aciklama = models.TextField(blank=True, null=True)
    devam_mi = models.BooleanField(default=False)
    tekrar_mi = models.BooleanField(default=False)
    tamamla_mi = models.BooleanField(default=False)
    ilk_dosya = models.FileField(upload_to='raporlar/', blank=True, null=True)
    sonuc_dosya = models.FileField(upload_to='raporlar/', blank=True, null=True)
    def __str__(self):
        return(self.denetim_adi)

class yazi(models.Model):
    yazi = models.CharField(max_length=1500)
    denetim = models.ForeignKey(denetim, on_delete=models.CASCADE)
    def __str__(self):
        return(self.denetim)

class kucukresim(models.Model):
    kullanici = models.ForeignKey(User, related_name='resim_ceken', on_delete=models.CASCADE)
    foto_kucuk = models.ImageField(upload_to='xyz/kucukresim/%Y/%m/%d/',blank=True, null=True,)

def upload_location(instance, filename):
    return "%s%s" %(instance.id, filename)

class sonuc_detay(models.Model):
    denetim = models.ForeignKey(denetim, on_delete=models.PROTECT)
    bolum = models.ForeignKey(bolum, on_delete=models.PROTECT)
    detay = models.ForeignKey(detay, on_delete=models.PROTECT)
    puanlama_turu = models.CharField(max_length=1, choices=PUANLAMA_TURU, default="A")
    onluk = models.CharField(max_length=2, choices=ONLUK, blank=True, null=True)
    beslik = models.CharField(max_length=1, choices=BESLIK, blank=True, null=True)
    ikilik = models.CharField(max_length=1, choices=IKILIK, blank=True, null=True)
    puan = models.IntegerField(blank=True, null=True)
    denetim_disi = models.CharField(max_length=1, choices=EVETHAYIR, default="H")
    resim_varmi = models.CharField(max_length=1, choices=EVETHAYIR, default="H")
    aciklama = models.CharField(max_length=100, blank=True, null=True)
    #foto = models.ImageField(upload_to='xyz/%Y/%m/%d/',blank=True, null=True, height_field="height_field", width_field="width_field")
    foto = models.ImageField(upload_to='xyz/%Y/%m/%d/',blank=True, null=True)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    tamam = models.CharField(max_length=1, choices=EVETHAYIR, default="H")
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(default=datetime.now())
    def __str__(self):
        return(self.denetim.denetim_adi)

class sonuc_bolum(models.Model):
    denetim = models.ForeignKey(denetim, on_delete=models.PROTECT)
    bolum = models.ForeignKey(bolum, on_delete=models.PROTECT)
    rutindenetci = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    tamam = models.CharField(max_length=1, choices=EVETHAYIR, default="H")
    def __str__(self):
        return(self.bolum.bolum_adi)

class sonuc_takipci(models.Model):
    denetim = models.ForeignKey(denetim, on_delete=models.PROTECT)
    takipci = models.ForeignKey(User, related_name='takipci', on_delete=models.CASCADE)
    def __str__(self):
        return(self.takipci.username)

class acil(models.Model):
    denetim = models.ForeignKey(denetim, on_delete=models.PROTECT)
    konu = models.CharField(max_length=100)
    aciklama = models.TextField()
    sonuc = models.TextField()
    acik_kapandi = models.CharField(max_length=1, choices=ACIKKAPANDI, default="A")
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(default=datetime.now())
    def __str__(self):
        return(self.denetim.denetim_adi)

class isaretler(models.Model):
    bolum_listesi_flag = models.BooleanField(default=True)
