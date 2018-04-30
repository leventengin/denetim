
from django.db import models
from webservice.models import Memnuniyet, BlogPost, MacPost
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
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    tip = models.CharField(max_length=2, default="A")
    timestamp = models.CharField(max_length=30)


@receiver(post_save, sender=Memnuniyet)
def create_notif_mem(sender, instance, **kwargs):
    print("receiver post save memnuniyet................")
    mac_no = instance.mac_no
    tipi = instance.tipi
    oy = instance.oy
    t_stamp = str(datetime.datetime.now())
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
    if tipi == "1" and oy == "3":
        title = "müşteri memnuniyetsizliği"
        message = mac_no + "  cihazından  " + sebep_yazi + "  sebebiyle  gelen memnuniyetsizlik var."
        Notification.objects.create(title=title, message=message, timestamp=t_stamp)
