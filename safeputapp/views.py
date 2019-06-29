# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect

from django.core.mail import send_mail
from django.conf import settings

# Belge işlemleri için eklenen django kütüphaneleri.
#from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
#from django.core.files.storage import FileSystemStorage

# Zaman işlemleri için eklenen python kütüphanesi.
import datetime

# Üstünde işlem yapacağımız modelleri ekliyoruz.
from .models import Firma, Is, Personel, Belge, BelgeDurum, Eposta, Kullanici, GuvenlikSeviye, IsDurum

# Belgelerin kayıt edileceği konum
#fs = FileSystemStorage(location='documents/')

# Create your views here.

## Temel

def index(request):

    request.session['kullanici'] = ""

    return render(request, "index.html")

## Anasayfayı ayarlar. Eğer session devam ediyorsa anasayfaya gider. Session yoksa giriş sayfasına gider.
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

## Kullanıcı çıkışı yapar ve giriş sayfasına geri döner.
def cikisYap(request):

    request.session['kullanici'] = ""

    return render(request, "index.html")

## Eposta

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

def epostaSil(request, id):

    eposta = get_object_or_404(Eposta, id = id)

    eposta.aktifmi = False

    eposta.save()

    return redirect("/epostaListe")

## Firma

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

def firmaSil(request, id):

    firma = get_object_or_404(Firma, id = id)

    firma.aktifmi = False

    firma.save()

    return redirect("/firmaListe")

## Is

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

            baglanti = "http://127.0.0.1:8000/isAnasayfa/" + str(yeniIs.id)

            Is.objects.filter( id = yeniIs.id ).update( baglanti = baglanti )

            return HttpResponseRedirect(request.path_info, { "firmalar" : firmalar, "seviyeler" : guvenlikSeviyeleri } )
        else:
            
            return render( request, "isEkle.html", { "firmalar" : firmalar, "seviyeler" : guvenlikSeviyeleri, "alert" : "İş ekleme işlemi başarısız oldu. Tüm alanları doğru şekilde doldurup tekrar deneyin." })

    else:

        return render(request, "isEkle.html", { "firmalar" : firmalar, "seviyeler" : guvenlikSeviyeleri })
        
def isSil(request, id):

    mevcutIs = get_object_or_404(Is, id = id)

    mevcutIs.aktifmi = False

    mevcutIs.save()

    return redirect("/isListe")

def isDetay(request, id):

    mevcutIs = get_object_or_404(Is, id = id)

    personeller = Personel.objects.filter(is_id = id)

    return render(request, "isDetay.html", { "mevcutIs" : mevcutIs, "personeller" : personeller })


def isAnasayfa(request, id):

    mevcutIs = get_object_or_404(Is, id = id)

    request.session['mevcutIs'] = mevcutIs.id

    return render(request, "isAnasayfa.html", { "mevcutIs" : mevcutIs })

def personelListe(request):
    personeller = Personel.objects.filter(is_id = request.session["mevcutIs"]).filter(aktifmi = True)
    return render(request, "personelListe.html", {"mevcutIs" : request.session['mevcutIs'], "personeller" : personeller})

def personelEkle(request):

    ad = request.POST.get("ad")
    soyad = request.POST.get("soyad")
    adres = request.POST.get("adres")
    telefon = request.POST.get("telefon")
    eposta = request.POST.get("eposta")
    tcno = request.POST.get("tcno")
    ehliyet_no = request.POST.get("ehliyet_no")
    kan_grubu = request.POST.get("kan_grubu")
    sgk_no = request.POST.get("sgk_no")
    is_id = request.session['mevcutIs']

    if request.POST.get("ekle"):
        if ad and soyad and adres and telefon and eposta and tcno and ehliyet_no and kan_grubu and sgk_no and is_id:

            mevcutIs = Is.objects.get(id = is_id)

            if not Personel.objects.filter(tcno = tcno):

                yeniPersonel = Personel(ad = ad, soyad = soyad, adres = adres, telefon = telefon, eposta = eposta, tcno = tcno, ehliyet_no = ehliyet_no, kan_grubu = kan_grubu, sgk_no = sgk_no, is_id = mevcutIs)

                yeniPersonel.save()

                return  render(request, "personelEkle.html", {"alert" : "Yeni personel başarılı bir şekilde eklendi.", "alertStatus" : True})
            else:
                return render(request, "personelEkle.html",
                              {"alert": "Aynı personel ikinci kez eklenemez. TC numarasının değiştirip tekrar deneyin.", "alertStatus": False})
        else:
            return render(request, "personelEkle.html",
                          {"alert": "Personel ekleme işlemi başarısız! Tüm alanları doldurup tekrar deneyin.", "alertStatus": False})
    else:
        return  render(request, "personelEkle.html")


def personelSil(request, id):

    personel = get_object_or_404(Personel, id = id)

    personel.aktifmi = False

    personel.save()

    return redirect("/personelListe")

def personelBelgeler(request, id):

    personel = get_object_or_404(Personel, id = id)

    belgeler = Belge.objects.filter(personel_id = id)

    return  render(request, "personelBelgeler.html", { "personel" : personel, "belgeler" : belgeler, "mevcutIs" : personel.is_id.id })

def belgeListe(request):

    belgeler = Belge.objects.filter(aktifmi = True)

    return render(request, "belgeListe.html", { "mevcutIs" : request.session['mevcutIs'], "belgeler" : belgeler })

def belgeEkle(request):

    personeller = Personel.objects.filter(is_id = request.session['mevcutIs'])

    ad = request.POST.get("ad")
    aciklama = request.POST.get("aciklama")
    personel_id = request.POST.get("personel")
    belge = request.FILES.get("belge")
    belge_durum = BelgeDurum.objects.get(ad = "Onay Bekliyor")

    if request.POST.get("ekle") :

        print ("Bilgiler")
        print (ad)
        print (aciklama)
        print (personel_id)
        print (belge.size)
        print (belge_durum)

        if ad and aciklama and personel_id and belge :

            if not Belge.objects.filter(belge = belge):

                path = default_storage.save('documents/'+belge.name , ContentFile(belge.read()))

                personel = Personel.objects.get(id = personel_id)

                belge = Belge(ad = ad, aciklama = aciklama, personel_id = personel, belge = path, belge_durum = belge_durum)

                belge.save()

                return render(request, "belgeEkle.html", {"personeller": personeller, "alert" : "Belge ekleme işlemi başarılı.", "alertStatus" : True})

            else :

                return render(request, "belgeEkle.html", {"personeller": personeller, "alert" : "Belge ekleme işlemi başarısız! Aynı belgeyi ikinci defa yükleyemezsiniz. Farklı bir belge yükleyerek tekrar deneyin.", "alertStatus" : False})
        else:
            return render(request, "belgeEkle.html",
                          {"personeller": personeller, "alert": "Belge ekleme işlemi başarısız! Tüm alanları doldurup tekrar deneyin.", "alertStatus": False})
    else:
        return render(request, "belgeEkle.html", { "personeller" : personeller})

def belgeSil(request, id):

    belge = get_object_or_404(Belge, id = id)

    belge.aktifmi = False

    belge.save()

    return redirect("/belgeListe")