from django.contrib import admin

from .models import Memnuniyet
from .models import Operasyon_Data, Denetim_Data, Ariza_Data
from .models import rfid_dosyasi, yer_updown



admin.site.register(Memnuniyet)
admin.site.register(Operasyon_Data)
admin.site.register(Denetim_Data)
admin.site.register(Ariza_Data)
admin.site.register(rfid_dosyasi)
admin.site.register(yer_updown)
