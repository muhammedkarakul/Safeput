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
from safeputapp.views import index, anasayfa, cikisYap, epostaGonder, epostaListe, epostaSil, firmaListe, firmaEkle, firmaSil, isListe, isEkle, isAnasayfa, isSil, personelListe, personelEkle, personelSil, belgeListe, belgeEkle

urlpatterns = [

    ## Temel
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),

    ## Panel
    url(r'^anasayfa', anasayfa),
    url(r'^cikisYap', cikisYap),

    ## Eposta
    url(r'^epostaGonder', epostaGonder),
    url(r'^epostaListe', epostaListe),
    url(r'^epostaSil/(?P<id>\d+)', epostaSil),

    ## Firma
    url(r'^firmaListe', firmaListe),
    url(r'^firmaEkle', firmaEkle),
    url(r'^firmaSil/(?P<id>\d+)', firmaSil),

    ## Is
    url(r'^isListe', isListe),
    url(r'^isEkle', isEkle),
    url(r'^isAnasayfa/(?P<id>\d+)', isAnasayfa),
    url(r'^isSil/(?P<id>\d+)', isSil),

    ## IsPanel
    url(r'^personelListe', personelListe),

    ## Personel
    url(r'^personelListe', personelListe),
    url(r'^personelEkle', personelEkle),
    url(r'^personelSil/(?P<id>\d+)', personelSil),

    ## Belge
    url(r'^belgeListe', belgeListe),
    url(r'^belgeEkle', belgeEkle),

]
