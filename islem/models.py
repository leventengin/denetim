from django.db import models
from django.contrib.auth.models import User, Group
#from datetime import datetime, date
import datetime
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from gm2m import GM2MField
from decimal import Decimal

EVETHAYIR = (
('E', 'Evet'),
('H', 'Hayır'),
)

ACIKKAPANDI = (
('A', 'Açık'),
('K', 'Kapandı'),
)

OPERASYONDIGER = (
('O', 'Operasyon'),
('D', 'Diğer'),
)

DENETCIPROJE = (
('D', 'Denetçi'),
('P', 'Proje'),
)

RUTINPLANLI = (
('P', 'Planlı'),
('R', 'Rutin'),
('S', 'Sıralı'),
('C', 'Checklist'),
('D', 'İşlem'),
)


PUANLAMA_TURU = (
('A', 'Onluk'),
('B', 'Beşlik'),
('C', 'İkilik'),
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

OPR_KULLANICI_TIPI = (
('Opr', 'Operasyon Elemanı'),
('Sef', 'Alan Şefi'),
('Pry', 'Proje Yöneticisi'),
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
    proje = models.ForeignKey('proje', on_delete=models.PROTECT)
    denetci = models.CharField(max_length=1, choices=EVETHAYIR, default="H")
    denetim_grup_yetkilisi = models.CharField(max_length=1, choices=EVETHAYIR, default="H")
    opr_gorev_tipi = models.CharField(max_length=3, choices=OPR_KULLANICI_TIPI, blank=True, null=True)
    operasyon_merkezyon = models.CharField(max_length=1, choices=EVETHAYIR, default="H")
    isletme_projeyon = models.CharField(max_length=1, choices=EVETHAYIR, default="H")
    profil_resmi = models.ImageField(upload_to='xyz/profile_resmi/%Y/%m/%d/',blank=True, null=True,)
    def __str__(self):
        return(self.user.username)

#
# operasyon görevlisi ise ie opr_gorev_tipi tanımlı ise veya işletme proje yöneticisi ise proje girilmiş olmalı
# işletme proje yöneticisi ise tüm projelerden seçecek, operasyon görevlisi ise kendi şirket projelerinden
# operasyon elemanları şu andaki sistemde sadece rfid içinde isim olarak tutuluyor, sisteme user kayıtları yok
#

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
    sil = models.BooleanField(default=False)
    def __str__(self):
        return '%s-%s' % (self.detay_kodu, self.detay_adi)
        #return(self.detay_adi)

"""
class proje_tipi(models.Model):
    p_tipi = models.CharField(max_length=200)
    def __str__(self):
        return(self.p_tipi)
"""


class proje(models.Model):
    proje_adi = models.CharField(max_length=200)
    #p_tipi = models.ForeignKey(proje_tipi, on_delete=models.PROTECT)
    sirket = models.ForeignKey(sirket, on_delete=models.PROTECT)
    ilgililer = models.ManyToManyField(User, related_name='ilgililer')
    proje_yonetici = models.ForeignKey(User, related_name='yonetici',  on_delete=models.CASCADE)
    def __str__(self):
        return(self.proje_adi)



class proje_alanlari(models.Model):
    proje = models.ForeignKey(proje, on_delete=models.PROTECT)
    alan = models.CharField(max_length=200)
    def __str__(self):
        return '%s-%s' % (self.proje, self.alan)


class yer(models.Model):
    proje_alanlari = models.ForeignKey(proje_alanlari, on_delete=models.PROTECT)
    yer_adi = models.CharField(max_length=200)
    mac_no = models.IntegerField()
    opr_basl = models.TimeField(default=datetime.time(8,0,0))
    opr_son = models.TimeField(default=datetime.time(22,0,0))
    opr_delta = models.TimeField(default=datetime.time(0,30,0))
    den_basl = models.TimeField(default=datetime.time(10,0,0))
    den_son = models.TimeField(default=datetime.time(22,0,0))
    den_delta = models.TimeField(default=datetime.time(2,0,0))
    def __str__(self):
        return str(self.yer_mac)


class plan_opr_gun(models.Model):
    yer = models.ForeignKey(yer, on_delete=models.PROTECT)
    gun = models.CharField(max_length=3, choices=GUNLER)
    zaman = models.TimeField()
    def __str__(self):
        return '%s-%s-%s' % (self.yer, self.gun, self.zaman)

class plan_den_gun(models.Model):
    yer = models.ForeignKey(yer, on_delete=models.PROTECT)
    gun = models.CharField(max_length=3, choices=GUNLER)
    zaman = models.TimeField()
    def __str__(self):
        return '%s-%s-%s' % (self.yer, self.gun, self.zaman)

class ariza_tipi(models.Model):
    ariza_tipi = models.CharField(max_length=200)
    def __str__(self):
        return(self.grup_adi)


class ariza(models.Model):
    ariza_tipi = models.ForeignKey(ariza_tipi, on_delete=models.PROTECT)
    yer = models.ForeignKey(yer, on_delete=models.PROTECT)
    tarih = models.DateField(_("Date"), default=datetime.date.today)
    def __str__(self):
        return(self.ariza)


class denetim(models.Model):
    denetim_adi = models.CharField(max_length=100)
    proje = models.ForeignKey(proje, on_delete=models.PROTECT)
    rutin_planli = models.CharField(max_length=1, choices=RUTINPLANLI)
    r_erisim = models.IntegerField(blank=True, null=True)
    denetci = models.ForeignKey(User, related_name='denetci', on_delete=models.CASCADE, null=True)
    tipi = models.ForeignKey(tipi, on_delete=models.PROTECT)
    durum = models.CharField(max_length=1, default="A")
    yaratim_tarihi = models.DateField(_("Date"), default=datetime.date.today)
    yaratan = models.ForeignKey(User, related_name='yaratan', on_delete=models.CASCADE)
    hedef_baslangic = models.DateField(blank=True, null=True)
    hedef_bitis = models.DateField(blank=True, null=True)
    gerc_baslangic = models.DateField(blank=True, null=True)
    gerc_bitis = models.DateField(blank=True, null=True)
    fiili_kapanis = models.DateField(blank=True, null=True)
    aciklama = models.TextField(blank=True, null=True)
    rutindenetci = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    yazi_varmi = models.CharField(max_length=1, choices=EVETHAYIR, default="H")
    rapor_yazi = models.TextField(blank=True, null=True)
    devam_mi = models.BooleanField(default=False)
    tekrar_mi = models.BooleanField(default=False)
    tamamla_mi = models.BooleanField(default=False)
    soru_adedi = models.IntegerField(default=0)
    dd_adedi = models.IntegerField(default=0)
    net_adet = models.IntegerField(default=0)
    toplam_puan = models.IntegerField(default=0)
    ortalama_puan = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    ilk_dosya = models.FileField(upload_to='raporlar/', blank=True, null=True)
    sonuc_dosya = models.FileField(upload_to='raporlar/', blank=True, null=True)
    def __str__(self):
        return(self.denetim_adi)

class yazi(models.Model):
    yazi = models.CharField(max_length=1500)
    denetim = models.ForeignKey(denetim, on_delete=models.CASCADE)
    def __str__(self):
        return(self.denetim)

class qrdosyasi(models.Model):
    qr_deger = models.CharField(max_length=50)
    denetim = models.ForeignKey(denetim, on_delete=models.CASCADE)
    def __str__(self):
        return(self.qr_deger)


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
    timestamp = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return(self.denetim.denetim_adi)

class sonuc_bolum(models.Model):
    denetim = models.ForeignKey(denetim, on_delete=models.PROTECT)
    bolum = models.ForeignKey(bolum, on_delete=models.PROTECT)
    rutindenetci = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    tamam = models.CharField(max_length=1, choices=EVETHAYIR, default="H")
    soru_adedi = models.IntegerField(default=0)
    dd_adedi = models.IntegerField(default=0)
    net_adet = models.IntegerField(default=0)
    toplam_puan = models.IntegerField(default=0)
    ortalama_puan = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    def __str__(self):
        return(self.bolum.bolum_adi)


class sonuc_takipci(models.Model):
    denetim = models.ForeignKey(denetim, on_delete=models.PROTECT)
    takipci = models.ForeignKey(User, related_name='takipci', on_delete=models.CASCADE)
    def __str__(self):
        return(self.takipci.username)


class sonuc_denetci(models.Model):
    denetim = models.ForeignKey(denetim, on_delete=models.PROTECT)
    denetci = models.ForeignKey(User, related_name='sonuc_denetci', on_delete=models.CASCADE)
    def __str__(self):
        return(self.denetci.username)


class sonuc_operator(models.Model):
    denetim = models.ForeignKey(denetim, on_delete=models.PROTECT)
    operator = models.ForeignKey(User, related_name='operator', on_delete=models.CASCADE)
    def __str__(self):
        return(self.operator.username)


class acil(models.Model):
    denetim = models.ForeignKey(denetim, on_delete=models.PROTECT)
    konu = models.CharField(max_length=100)
    aciklama = models.TextField()
    sonuc = models.TextField()
    acik_kapandi = models.CharField(max_length=1, choices=ACIKKAPANDI, default="A")
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return(self.denetim.denetim_adi)

class isaretler(models.Model):
    bolum_listesi_flag = models.BooleanField(default=True)
