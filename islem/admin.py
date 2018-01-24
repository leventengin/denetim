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
from .models import musteri
from .models import tipi
from .models import bolum
from .models import detay
from .models import denetim
from .models import gozlemci
from .models import sonuc
from .models import sonuc_bolum
from .models import kucukresim
from .models import acil
from resimyukle.models import Resim


admin.site.register(grup)
admin.site.register(sirket)
admin.site.register(musteri)
admin.site.register(tipi)
admin.site.register(bolum)
admin.site.register(detay)
admin.site.register(denetim)
admin.site.register(gozlemci)
admin.site.register(sonuc)
admin.site.register(sonuc_bolum)
admin.site.register(Resim)
admin.site.register(kucukresim)
admin.site.register(acil)
