
from django.db import models
from webservice.models import Memnuniyet, Denetim_Data, Ariza_Data, rfid_dosyasi
from islem.models import yer
from django.contrib.auth.models import User, Group
#from datetime import datetime, date
import datetime
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from gm2m import GM2MField
from decimal import Decimal
from django.contrib.auth.models import User, Group


class Notification(models.Model):
    title = models.CharField(max_length=256)
    proje = models.ForeignKey('islem.proje', on_delete=models.PROTECT)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    tip = models.CharField(max_length=2, default="A")
    timestamp = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return '%s-%s' % (self.proje, self.timestamp)


@receiver(post_save, sender=Memnuniyet)
def create_notif_mem(sender, instance, **kwargs):
    print("receiver post save memnuniyet................")
    mac_no = instance.mac_no
    proje = instance.proje
    proje_no = instance.proje.id
    yer_obj = yer.objects.filter(mac_no=mac_no).first()
    if yer_obj:
        yer_yaz = str(yer_obj.yer_adi)
    else:
        yer_yaz = str(mac_no)

    tipi = instance.tipi
    oy = instance.oy
    t_stamp = instance.gelen_tarih
    print("t stamp...", t_stamp)


    sebep = instance.sebep
    if sebep == "1":
        sebep_yazi = "sabunluk"
    if sebep == "2":
        sebep_yazi = "lavabo"
    if sebep == "3":
        sebep_yazi = "havlu"
    if sebep == "4":
        sebep_yazi = "koku"
    if sebep == "5":
        sebep_yazi = "tuvalet"
    if sebep == "6":
        sebep_yazi = "tuvalet kağıdı"

    print("macno", mac_no, "tipi:", tipi, "oy:", oy, "sebep:", sebep)
    print("proje no", proje_no)
    print("proje", proje)
    if tipi == "1" and oy == "3":
        title = "müşteri memnuniyetsizliği"
        message =  yer_yaz + " " + sebep_yazi + "  sebebiyle şikayet var."
        print("yazılan mesaj...", message)
        Notification.objects.create(title=title, proje_id=proje_no,  message=message, timestamp=t_stamp)


@receiver(post_save, sender=Ariza_Data)
def create_notif_ariza(sender, instance, **kwargs):
    print("receiver post save arıza data................")

    mac_no = instance.mac_no
    tipi = instance.tipi
    proje = instance.proje
    proje_no = instance.proje.id
    yer_obj = yer.objects.filter(mac_no=mac_no).first()
    if yer_obj:
        yer_yaz = str(yer_obj.yer_adi)
    else:
        yer_yaz = str(mac_no)

    t_stamp = instance.gelen_tarih

    rfid_no = instance.rfid_no

    rfid_obj = rfid_dosyasi.objects.filter(rfid_no=rfid_no).first()

    if rfid_obj:
        adi = rfid_obj.adi
        soyadi = rfid_obj.soyadi
    else:
        adi = ""
        soyadi = ""



    sebep = instance.sebep
    if sebep == "1":
        sebep_yazi = "mekanik"
    if sebep == "2":
        sebep_yazi = "elektrik"
    if sebep == "3":
        sebep_yazi = "su"
    if sebep == "4":
        sebep_yazi = "ayna"


    print("macno", mac_no, "tipi:", tipi, "sebep:", sebep)
    print("proje no", proje_no)
    print("proje", proje)

    title = "arıza bildirimi  "
    message =  yer_yaz + " " + sebep_yazi + "  arıza bildirimi  " + adi + " " + soyadi
    print("yazılan mesaj...", message)
    Notification.objects.create(title=title, proje_id=proje_no,  message=message, timestamp=t_stamp)



@receiver(post_save, sender=Denetim_Data)
def create_notif_densaha(sender, instance, **kwargs):
    print("receiver post save denetim saha data................")

    mac_no = instance.mac_no
    tipi = instance.tipi
    proje = instance.proje
    proje_no = instance.proje.id
    yer_obj = yer.objects.filter(mac_no=mac_no).first()

    if yer_obj:
        yer_yaz = str(yer_obj.yer_adi)
    else:
        yer_yaz = str(mac_no)

    t_stamp = instance.gelen_tarih

    rfid_no = instance.rfid_no

    rfid_obj = rfid_dosyasi.objects.filter(rfid_no=rfid_no).first()

    if rfid_obj:
        adi = rfid_obj.adi
        soyadi = rfid_obj.soyadi
    else:
        adi = ""
        soyadi = ""

    kod = instance.kod

    sayi = int(kod)
    print("işte gelen kodun sayısal hali...", sayi)

    if sayi == 0:
        pass
    else:
        sabun = sayi // 32
        sayi = sayi % 32
        lavabo = sayi // 16
        sayi = sayi % 16
        havlu = sayi // 8
        sayi = sayi % 8
        koku = sayi // 4
        sayi = sayi % 4
        tuvalet = sayi // 2
        kagit = sayi % 2

        aciklama = ""
        if sabun == 1:
            aciklama = aciklama + " sabun -"
        if lavabo == 1:
            aciklama = aciklama + " lavabo -"
        if havlu == 1:
            aciklama = aciklama + " havlu -"
        if koku == 1:
            aciklama = aciklama + " koku -"
        if tuvalet == 1:
            aciklama = aciklama + " tuvalet -"
        if kagit == 1:
            aciklama = aciklama + " kağıt -"



        print("macno", mac_no)
        print("proje no", proje_no)
        print("proje", proje)

        title = "denetim bildirimi  "
        message =  yer_yaz + " " + aciklama + "  denetim bildirimi  " + adi + " " + soyadi
        print("yazılan mesaj...", message)
        Notification.objects.create(title=title, proje_id=proje_no,  message=message, timestamp=t_stamp)
