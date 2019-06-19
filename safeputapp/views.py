# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect

from django.core.mail import send_mail
from django.conf import settings

import datetime

# Üstünde işlem yapacağımız modelleri ekliyoruz.
from .models import Firma, Is, Personel, Belge, BelgeDurum, Eposta, Kullanici, GuvenlikSeviye, IsDurum

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

    baslik = request.POST.get("baslik")
    mesaj = request.POST.get("mesaj")
    aktifmi = True
    is_id = request.POST.get("is_id")
    olusturma_tarihi = datetime.datetime.now()

    if request.POST.get("gonder"):

        if baslik and mesaj and is_id and aktifmi and olusturma_tarihi:

            is_nesnesi = Is.objects.filter(id = request.POST.get("is_id")).first()

            print("FIRMA ID")
            print(is_nesnesi.firma_id)

            firma_nesnesi = Firma.objects.get(unvan = is_nesnesi.firma_id)
            baglanti_link = is_nesnesi.baglanti

            print("FİRMA EPOSTA")
            print(firma_nesnesi.eposta)

            yeniEposta = Eposta(baslik = baslik, mesaj = mesaj, is_id = is_nesnesi, baglanti_link = baglanti_link, aktifmi = aktifmi, olusturma_tarihi = olusturma_tarihi)

            yeniEposta.save()

            epostaMesaj = mesaj + "\n\n" + "Tanım:\n" + is_nesnesi.tanim + "\n\n" + "Bağlantı:\n" + is_nesnesi.baglanti

            send_mail( yeniEposta.baslik, epostaMesaj, "muhammedkarakul@gmail.com", [ firma_nesnesi.eposta ])


            return HttpResponseRedirect(request.path_info, { "isler" : isler } )

        else:
            
            return render( request, "epostaGonder.html", { "isler" : isler }, { "alert" : "E-posta gönderme işlemi başarısız oldu. Tüm alanları doğru şekilde doldurup tekrar deneyin." })

    else:
        
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


    if request.POST.get("ekle") :
        if kutuk_no and unvan and adres and posta_kodu and sehir and telefon and faks and eposta and aktifmi and olusturma_tarihi :
            yeniFirma = Firma(unvan = unvan, kutuk_no = kutuk_no, adres = adres, posta_kodu = posta_kodu, sehir = sehir, telefon = telefon, faks = faks, eposta = eposta, aktifmi = aktifmi, olusturma_tarihi = olusturma_tarihi)
            yeniFirma.save()
            return render( request, "firmaEkle.html", { "firma" : yeniFirma, "alert" : "Firma ekleme işlemi başarılı." } )
        else:    
            return render( request, "firmaEkle.html", { "alert" : "Firma ekleme işlemi başarısız oldu. Tüm alanları doğru şekilde doldurup tekrar deneyin." })
    else:
        return render( request, "firmaEkle.html")

def isListe(request):

    isler = Is.objects.all()

    return render(request, "isListe.html", { "isler" : isler })

def isEkle(request):

    isDurumlari = IsDurum.objects.all().first()

    ad = request.POST.get("ad")
    tanim = request.POST.get("tanim")
    fatura_no = request.POST.get("fatura_no")
    guvenlik_seviye = GuvenlikSeviye.objects.filter(id = request.POST.get("guvenlik_seviye")).first() #GuvenlikSeviye.objects.filter( id = request.POST.get("guvenlik_seviye") )
    is_durum = isDurumlari
    aktifmi = True
    firma_id = Firma.objects.filter(id = request.POST.get("firma_id")).first() #Firma.objects.filter(id = request.POST.get("firma_id"))
    olusturma_tarihi = datetime.datetime.now()
    
    firmalar = Firma.objects.all()
    guvenlikSeviyeleri = GuvenlikSeviye.objects.all()

    if request.POST.get("ekle") :

        if ad and tanim and fatura_no and guvenlik_seviye and is_durum and aktifmi and firma_id and olusturma_tarihi:

            #print("PARAMETRELER")
            #print(ad + tanim + fatura_no + guvenlik_seviye + is_durum + aktifmi + firma_id + olusturma_tarihi)

            yeniIs = Is(ad = ad, tanim = tanim, fatura_no = fatura_no, guvenlik_seviye = guvenlik_seviye, is_durum = is_durum, aktifmi = aktifmi, firma_id = firma_id, olusturma_tarihi = olusturma_tarihi)
            
            yeniIs.save()

            baglanti = "http://127.0.0.1:8000/firmaAnasayfa/" + str(yeniIs.id)

            Is.objects.filter( id = yeniIs.id ).update( baglanti = baglanti )

            return HttpResponseRedirect(request.path_info, { "firmalar" : firmalar, "seviyeler" : guvenlikSeviyeleri } )
        else:
            
            return render( request, "isEkle.html", { "firmalar" : firmalar, "seviyeler" : guvenlikSeviyeleri, "alert" : "İş ekleme işlemi başarısız oldu. Tüm alanları doğru şekilde doldurup tekrar deneyin." })

    else:

        return render(request, "isEkle.html", { "firmalar" : firmalar, "seviyeler" : guvenlikSeviyeleri })
        

def firmaAnasayfa(request, id):

    mevcutIs = get_object_or_404(Is, id = id)

    request.session['mevcutIs'] = mevcutIs.id

    return render(request, "firma_anasayfa.html", { "mevcutIs" : mevcutIs })

def cikisYap(request):

    request.session['kullanici'] = ""

    return render(request, "index.html")
    