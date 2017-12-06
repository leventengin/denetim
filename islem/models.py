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

PUAN = (
('A', 'Çok İyi'),
('B', 'İyi'),
('C', 'Orta'),
('D', 'Kötü'),
)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    denetci = models.CharField(max_length=1, choices=EVETHAYIR)
    denetim_takipcisi = models.CharField(max_length=1, choices=EVETHAYIR)
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

class musteri(models.Model):
    musteri_adi = models.CharField(max_length=200)
    def __str__(self):
        return(self.musteri_adi)

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



class denetim(models.Model):
    denetim_adi = models.CharField(max_length=100)
    musteri = models.ForeignKey(musteri, on_delete=models.PROTECT)
    denetci = models.ForeignKey(User, related_name='denetci', on_delete=models.CASCADE)
    tipi = models.ForeignKey(tipi, on_delete=models.PROTECT)
    durum = models.CharField(max_length=1)
    yaratim_tarihi = models.DateField()
    yaratan = models.ForeignKey(User, related_name='yaratan', on_delete=models.CASCADE)
    hedef_baslangic = models.DateField()
    hedef_bitis = models.DateField()
    gerc_baslangic = models.DateField(blank=True, null=True)
    gerc_bitis = models.DateField(blank=True, null=True)
    fiili_kapanis = models.DateField(blank=True, null=True)
    aciklama = models.TextField(blank=True, null=True)
    devam_mi = models.BooleanField(default=False)
    tekrar_mi = models.BooleanField(default=False)
    tamamla_mi = models.BooleanField(default=False)
    ilk_dosya = models.FileField(upload_to='yuklemeler/', blank=True, null=True)
    sonuc_dosya = models.FileField(upload_to='yuklemeler/', blank=True, null=True)
    def __str__(self):
        return(self.denetim_adi)

class gozlemci(models.Model):
    denetim = models.ForeignKey(denetim, on_delete=models.PROTECT)
    gozlemci = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return(self.denetim.denetim_adi)


def upload_location(instance, filename):
    return "%s%s" %(instance.id, filename)

class sonuc(models.Model):
    denetim = models.ForeignKey(denetim, on_delete=models.PROTECT)
    bolum = models.ForeignKey(bolum, on_delete=models.PROTECT)
    detay = models.ForeignKey(detay, on_delete=models.PROTECT)
    sayi = models.CharField(max_length=1, choices=PUAN, default=None)
    aciklama = models.CharField(max_length=100, blank=True, null=True)
    #foto = models.ImageField(upload_to='upload_location/',blank=True, null=True, height_field="height_field", width_field="width_field")
    #foto = models.ImageField(upload_to='cekimler',blank=True, null=True, height_field="height_field", width_field="width_field")
    foto = models.ImageField(upload_to='xyz/%Y/%m/%d/',blank=True, null=True, height_field="height_field", width_field="width_field")
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
    tamam = models.CharField(max_length=1, choices=EVETHAYIR, default="H")
    def __str__(self):
        return(self.bolum.bolum_adi)


class grup(models.Model):
    grup_adi = models.CharField(max_length=200)
    def __str__(self):
        return(self.grup_adi)


class sirket(models.Model):
    sirket_adi = models.CharField(max_length=200)
    grubu = models.ForeignKey(grup, on_delete=models.PROTECT)
    def __str__(self):
        return(self.sirket_adi)
