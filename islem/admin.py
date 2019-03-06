from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',)
    list_select_related = ('profile', )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)



# register your models here ...

from .models import grup
from .models import sirket
from .models import proje
from .models import tipi
from .models import zon
from .models import bolum
from .models import detay
from .models import denetim
from .models import sonuc_detay
from .models import sonuc_bolum
from .models import sonuc_takipci
from .models import sonuc_resim
from .models import kucukresim
from .models import spv_yetkilisi
from .models import den_yetkilisi
from .models import acil
from .models import isaretler
from .models import qrdosyasi
from .models import yer
from .models import proje_alanlari
from .models import plan_opr_gun
from .models import plan_den_gun
from .models import eleman
from notification.models import Notification
from webservice.models import rfid_dosyasi
from webservice.models import yer_updown

admin.site.register(grup)
admin.site.register(sirket)
admin.site.register(proje)
admin.site.register(tipi)
admin.site.register(zon)
admin.site.register(bolum)
admin.site.register(detay)
admin.site.register(denetim)
admin.site.register(sonuc_detay)
admin.site.register(sonuc_bolum)
admin.site.register(sonuc_takipci)
admin.site.register(sonuc_resim)
admin.site.register(kucukresim)
admin.site.register(spv_yetkilisi)
admin.site.register(den_yetkilisi)
admin.site.register(acil)
admin.site.register(isaretler)
admin.site.register(qrdosyasi)
admin.site.register(yer)
admin.site.register(proje_alanlari)
admin.site.register(plan_opr_gun)
admin.site.register(plan_den_gun)
admin.site.register(Notification)
admin.site.register(eleman)

#admin.site.register(rfid_dosyasi)
#admin.site.register(yer_updown)
