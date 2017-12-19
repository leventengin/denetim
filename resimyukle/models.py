from django.db import models

# Create your models here.


#class ResimYukle(models.Model):
#    kucuk = models.ImageField('kucuk_resim')

class Resim(models.Model):
    kucuk_resim = models.ImageField('kucuk_resim')
