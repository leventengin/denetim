from django.contrib import admin

from .models import BlogPost, MacPost, Memnuniyet
from .models import Operasyon_Data, Denetim_Data, Ariza_Data

admin.site.register(BlogPost)
admin.site.register(MacPost)
admin.site.register(Memnuniyet)
admin.site.register(Operasyon_Data)
admin.site.register(Denetim_Data)
admin.site.register(Ariza_Data)
