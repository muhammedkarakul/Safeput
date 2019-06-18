# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

# Üstünde işlem yapacağımız modelleri ekliyoruz.
from .models import Firma, Is, Personel, Belge, BelgeDurum, Eposta, Kullanici

# Create your views here.

def index(request):

    request.session['kadi'] = ""

    return render(request, "index.html")

def anasayfa(request):
    if request.method == "GET":
        #GET tipi istekler buraya duser.

        #Ana sayfaya don.
        return redirect("/")

    else:
        #POST tipi istekler buraya dusur.

        if request.session['kadi'] :

            return render(request, "anasayfa.html")

        else: 

            kullaniciAd = request.POST.get("kadi")
            sifre = request.POST.get("sifre")

            # Form nesnemizin degerini almak.
            kullanici = Kullanici.objects.filter(ad = kullaniciAd, sifre = sifre)

            if not kullanici :
                return redirect("/", { "kullanici" : kullanici } )
            else:

                request.session['kadi'] = kullaniciAd

                return render(request, "anasayfa.html")


def eposta(request):

    # Anasayfada eposta sekmesine tıkladığında burası çalışacak

    # Is veri tabanındaki bütün nesneleri alır.
    isler = Is.objects.all()

    # Eposta sayfasına git. Is nesnelerini de sayfaya aktar.
    return render( request, "eposta.html", { "isler" : isler } )

def epostaGonder(request):

    return redirect("/anasayfa")


    #if request.method == "POST":
        # Eposta gönderim işlemi yapıldığında burası çalışacak
    #    return render(request, "anasayfa.html")
    
