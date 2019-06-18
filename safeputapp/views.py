# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

import datetime

# Üstünde işlem yapacağımız modelleri ekliyoruz.
from .models import Firma, Is, Personel, Belge, BelgeDurum, Eposta, Kullanici

# Create your views here.

def index(request):

    request.session['kullanici'] = ""

    return render(request, "index.html")

def anasayfa(request):

    if request.method == "GET":
        #GET tipi istekler buraya duser.

        #Ana sayfaya don.

        return render(request, "anasayfa.html")

    else:
        #POST tipi istekler buraya dusur.

        if request.session.get('kullanici'):

            return render(request, "anasayfa.html")

        else: 

            kullaniciAd = request.POST.get("kadi")
            sifre = request.POST.get("sifre")

            # Form nesnemizin degerini almak.
            kullanici = Kullanici.objects.filter(ad = kullaniciAd, sifre = sifre).first()

            if not kullanici :

                return render(request, "index.html", { "alert" : "Kullanıcı bulunamadı!" })

            else:

                request.session['kullanici'] = kullanici.id

                return render(request, "anasayfa.html")


def epostaGonder(request):

    # Anasayfada eposta sekmesine tıkladığında burası çalışacak

    # Is veri tabanındaki bütün nesneleri alır.
    isler = Is.objects.all()

    # Eposta sayfasına git. Is nesnelerini de sayfaya aktar.
    return render( request, "epostaGonder.html", { "isler" : isler } )
    
def epostaListe(request):

    epostalar = Eposta.objects.all()

    return render( request, "epostaListe.html", { "epostalar" : epostalar } )

def firmaListe(request):

    firmalar = Firma.objects.all()

    return render( request, "firmaListe.html", { "firmalar" : firmalar } )

def firmaEkle(request):
    kutuk_no = request.POST.get("kutuk_no")
    unvan = request.POST.get("unvan")
    adres = request.POST.get("adres")
    posta_kodu = request.POST.get("posta_kodu")
    sehir = request.POST.get("sehir")
    telefon = request.POST.get("telefon")
    faks = request.POST.get("faks")
    eposta = request.POST.get("eposta")
    aktifmi = True
    olusturma_tarihi = datetime.datetime.now()

    if kutuk_no and unvan and adres and posta_kodu and sehir and telefon and faks and eposta and aktifmi and olusturma_tarihi :
        yeniFirma = Firma(unvan = unvan, kutuk_no = kutuk_no, adres = adres, posta_kodu = posta_kodu, sehir = sehir, telefon = telefon, faks = faks, eposta = eposta)
    else:    
        

    return render( request, "firmaEkle.html")