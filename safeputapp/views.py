# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404

# Üstünde işlem yapacağımız modelleri ekliyoruz.
from .models import Firma, Is, Personel, Belge, BelgeDurum, Eposta, Kullanici

# Create your views here.

def index(request):
    return render(request, "index.html")

def kullaniciGiris(request):
    if request.method == "GET":
        #GET tipi istekler buraya duser.

        #Ana sayfaya don.
        return redirect("/")

    else:
        #POST tipi istekler buraya dusur.

        kullaniciAd = request.POST.get("kadi")
        sifre = request.POST.get("sifre")

        # Form nesnemizin degerini almak.
        kullanici = Kullanici.objects.filter(ad = kullaniciAd, sifre = sifre)

        if not kullanici :
            return redirect("/", { "kullanici" : kullanici } )
        else:
            return render(request, "anasayfa.html")

def eposta(request):

    # Anasayfada eposta sekmesine tıkladığında burası çalışacak

    # Is veri tabanındaki bütün objeleri alır.
    isler = Is.objects.all()

    return render( request, "eposta.html", { "isler" : isler } )

def epostaGonder(request):

    # Eposta gönderim işlemi yapıldığında burası çalışacak

    return render(request, "anasayfa.html")
