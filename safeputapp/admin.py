# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Firma, Is, Personel, Belge, BelgeDurum, Eposta, Kullanici, IsDurum, GuvenlikSeviye, GuvenlikBelgeTurleri, Guvenlik

# Register your models here.
admin.site.register(Firma)
admin.site.register(Is)
admin.site.register(Personel)
admin.site.register(Belge)
admin.site.register(BelgeDurum)
admin.site.register(Eposta)
admin.site.register(Kullanici)
admin.site.register(IsDurum)
admin.site.register(GuvenlikSeviye)
admin.site.register(GuvenlikBelgeTurleri)
admin.site.register(Guvenlik)
