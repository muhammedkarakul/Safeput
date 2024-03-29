"""safeput URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

# Dosyalarin yuklenecegi konumlari import ediyoruz.
from django.conf import settings
from django.conf.urls.static import static

from safeputapp.views import index, anasayfa, anasayfaGiris, cikisYap, epostaGonder, epostaListe, epostaSil, firmaListe, firmaEkle, firmaSil, firmaDetay, isListe, isEkle, isAnasayfa, isSil, isDetay, personelListe, personelEkle, personelSil, personelBelgeler, personelDetay, belgeListe, belgeEkle, belgeSil, belgeOnizle, belgeOnay, belgeRed, bilgilendirmeMailGonder, guvenlikGiris, guvenlikCikisYap, guvenlikVideo

urlpatterns = [

    ## Temel
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),

    ## Panel
    url(r'^anasayfaGiris', anasayfaGiris),
    url(r'^anasayfa', anasayfa),
    url(r'^cikisYap', cikisYap),

    ## Eposta
    url(r'^epostaGonder/(?P<id>\d+)', epostaGonder),
    url(r'^epostaListe', epostaListe),
    url(r'^epostaSil/(?P<id>\d+)', epostaSil),

    ## Firma
    url(r'^firmaListe', firmaListe),
    url(r'^firmaEkle', firmaEkle),
    url(r'^firmaSil/(?P<id>\d+)', firmaSil),
    url(r'^firmaDetay/(?P<id>\d+)', firmaDetay),

    ## Is
    url(r'^isListe', isListe),
    url(r'^isEkle/(?P<id>\d+)', isEkle),
    url(r'^isSil/(?P<id>\d+)', isSil),
    url(r'^isDetay/(?P<id>\d+)', isDetay),

    ## IsPanel
    url(r'^isAnasayfa/(?P<id>\d+)', isAnasayfa),

    ## Personel
    url(r'^personelListe/(?P<id>\d+)', personelListe),
    url(r'^personelEkle/(?P<id>\d+)', personelEkle),
    url(r'^personelSil/(?P<id>\d+)', personelSil),
    url(r'^personelBelgeler/(?P<id>\d+)', personelBelgeler),
    url(r'^personelDetay/(?P<id>\d+)', personelDetay),


    ## Belge
    url(r'^belgeListe', belgeListe),
    url(r'^belgeEkle/(?P<id>\d+)', belgeEkle),
    url(r'^belgeSil/(?P<id>\d+)', belgeSil),
    url(r'^belgeOnizle/(?P<id>\d+)', belgeOnizle),
    url(r'^belgeOnay/(?P<id>\d+)', belgeOnay),
    url(r'^belgeRed/(?P<id>\d+)', belgeRed),
    url(r'^bilgilendirmeMailGonder/(?P<id>\d+)', bilgilendirmeMailGonder),

    ## Guvenlik
    url(r'^guvenlikGiris', guvenlikGiris),
    url(r'^guvenlikCikisYap', guvenlikCikisYap),
    url(r'^guvenlikVideo', guvenlikVideo),

] + static(settings.DOCUMENTS_URL, document_root=settings.DOCUMENTS_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)