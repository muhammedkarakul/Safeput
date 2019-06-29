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

# Belge indirme işlemleri için eklenen python ve django kütüphaneleri
import os
from django.http import HttpResponse, Http404

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

def epostaGonder(request, id):

    # Anasayfada eposta sekmesine tıkladığında burası çalışacak

    # Is veri tabanındaki bütün nesneleri alır.
    #isler = Is.objects.all()

    baslik = request.POST.get("baslik")
    mesaj = request.POST.get("mesaj")
    aktifmi = True
    #is_id = request.POST.get("is_id")
    olusturma_tarihi = datetime.datetime.now()

    mevcutIs = get_object_or_404(Is, id = id)

    if request.POST.get("gonder"):

        if baslik and mesaj and mevcutIs and aktifmi and olusturma_tarihi:

            #is_nesnesi = Is.objects.filter(id = request.POST.get("is_id")).first()
            #mevcutIs = get_object_or_404(Is, id = is_id)

            print("FIRMA ID")
            print(mevcutIs.firma_id)

            #firma_nesnesi = Firma.objects.get(unvan = mevcutIs.firma_id)
            firma = get_object_or_404(Firma, id = mevcutIs.firma_id.id)
            baglanti_link = mevcutIs.baglanti

            print("FİRMA EPOSTA")
            print(mevcutIs.firma_id.eposta)

            yeniEposta = Eposta(baslik = baslik, mesaj = mesaj, is_id = mevcutIs, baglanti_link = baglanti_link, aktifmi = aktifmi, olusturma_tarihi = olusturma_tarihi)

            yeniEposta.save()

            epostaMesaj = mesaj + "\n\n" + "Tanım:\n" + mevcutIs.tanim + "\n\n" + "Bağlantı:\n" + mevcutIs.baglanti

            send_mail( yeniEposta.baslik, epostaMesaj, "muhammedkarakul@gmail.com", [ firma.eposta ])


            #return HttpResponseRedirect(request.path_info, { "mevcutIs" : mevcutIs } )
            return  render( request, "epostaGonder.html", { "mevcutIs" : mevcutIs, "alert" : "E-posta gönderme işlemi başarılı.", "alertState" : True })

        else:
            
            return render( request, "epostaGonder.html", { "mevcutIs" : mevcutIs, "alert" : "E-posta gönderme işlemi başarısız oldu. Tüm alanları doğru şekilde doldurup tekrar deneyin.", "alertState" : False })

    else:
        
    # Eposta sayfasına git. Is nesnelerini de sayfaya aktar.
        return render( request, "epostaGonder.html", { "mevcutIs" : mevcutIs } )
    
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
            return render( request, "firmaEkle.html", { "firma" : yeniFirma, "alert" : "Firma ekleme işlemi başarılı.", "alertState" : True } )
        else:    
            return render( request, "firmaEkle.html", { "alert" : "Firma ekleme işlemi başarısız oldu. Tüm alanları doğru şekilde doldurup tekrar deneyin.", "alertState" : False })
    else:
        return render( request, "firmaEkle.html")

def firmaSil(request, id):

    firma = get_object_or_404(Firma, id = id)

    firma.aktifmi = False

    firma.save()

    return redirect("/firmaListe")

def firmaDetay(request, id):

    firma = get_object_or_404(Firma, id = id)

    isler = Is.objects.filter(firma_id = id).filter(aktifmi = True)

    return render(request, "firmaDetay.html", { "firma" : firma, "isler" : isler })

## Is

def isListe(request):

    isler = Is.objects.all()

    return render(request, "isListe.html", { "isler" : isler })

def isEkle(request, id):

    isDurumlari = IsDurum.objects.all().first()

    ad = request.POST.get("ad")
    tanim = request.POST.get("tanim")
    fatura_no = request.POST.get("fatura_no")
    guvenlik_seviye = GuvenlikSeviye.objects.filter(id = request.POST.get("guvenlik_seviye")).first() #GuvenlikSeviye.objects.filter( id = request.POST.get("guvenlik_seviye") )
    is_durum = isDurumlari
    aktifmi = True
    #firma_id = Firma.objects.filter(id = request.POST.get("firma_id")).first() #Firma.objects.filter(id = request.POST.get("firma_id"))
    #firma_id = Firma.objects.filter(id = id)
    firma_id = get_object_or_404(Firma, id = id)
    olusturma_tarihi = datetime.datetime.now()
    
    #firmalar = Firma.objects.all()
    guvenlikSeviyeleri = GuvenlikSeviye.objects.all()

    if request.POST.get("ekle") :

        if ad and tanim and fatura_no and guvenlik_seviye and is_durum and aktifmi and firma_id and olusturma_tarihi:

            #print("PARAMETRELER")
            #print(ad + tanim + fatura_no + guvenlik_seviye + is_durum + aktifmi + firma_id + olusturma_tarihi)

            yeniIs = Is(ad = ad, tanim = tanim, fatura_no = fatura_no, guvenlik_seviye = guvenlik_seviye, is_durum = is_durum, aktifmi = aktifmi, firma_id = firma_id, olusturma_tarihi = olusturma_tarihi)
            
            yeniIs.save()

            baglanti = "http://127.0.0.1:8000/isAnasayfa/" + str(yeniIs.id)

            Is.objects.filter( id = yeniIs.id ).update( baglanti = baglanti )

            #return HttpResponseRedirect(request.path_info, { "firma" : firma_id, "seviyeler" : guvenlikSeviyeleri, "alert" : "İş başarılı bir şekilde eklendi.", "alertState" : True } )
            return render(request, "isEkle.html", {"firma": firma_id, "seviyeler": guvenlikSeviyeleri, "alert": "İş başarılı bir şekilde eklendi.", "alertState": True})
        else:
            
            return render( request, "isEkle.html", { "firma" : firma_id, "seviyeler" : guvenlikSeviyeleri, "alert" : "İş ekleme işlemi başarısız oldu. Tüm alanları doğru şekilde doldurup tekrar deneyin.", "alertState" : False })

    else:

        return render(request, "isEkle.html", { "firma" : firma_id, "seviyeler" : guvenlikSeviyeleri })
        
def isSil(request, id):

    mevcutIs = get_object_or_404(Is, id = id)

    mevcutIs.aktifmi = False

    mevcutIs.save()

    return redirect("/isListe")

def isDetay(request, id):

    print ("IS ID: " + id)

    mevcutIs = get_object_or_404(Is, id = id)

    epostalar = Eposta.objects.filter(is_id = id).filter(aktifmi = True)
    #epostalar = get_object_or_404(Eposta, is_id = id)

    personeller = Personel.objects.filter(is_id = id).filter(aktifmi = True)
    #personeller = get_object_or_404(Personel, is_id = id)

    return render(request, "isDetay.html", { "mevcutIs" : mevcutIs, "personeller" : personeller, "epostalar" : epostalar })


def isAnasayfa(request, id):

    mevcutIs = get_object_or_404(Is, id = id)

    request.session['mevcutIs'] = mevcutIs.id

    return render(request, "isAnasayfa.html", { "mevcutIs" : mevcutIs })

def personelListe(request, id):

    personeller = Personel.objects.filter(is_id = id).filter(aktifmi = True)

    return render(request, "personelListe.html", {"mevcutIs" : request.session['mevcutIs'], "personeller" : personeller})

def personelEkle(request, id):

    ad = request.POST.get("ad")
    soyad = request.POST.get("soyad")
    adres = request.POST.get("adres")
    telefon = request.POST.get("telefon")
    eposta = request.POST.get("eposta")
    tcno = request.POST.get("tcno")
    ehliyet_no = request.POST.get("ehliyet_no")
    kan_grubu = request.POST.get("kan_grubu")
    sgk_no = request.POST.get("sgk_no")
    #is_id = request.session['mevcutIs']
    mevcutIs = get_object_or_404(Is, id = id)

    if request.POST.get("ekle"):
        if ad and soyad and adres and telefon and eposta and tcno and ehliyet_no and kan_grubu and sgk_no:

            #mevcutIs = Is.objects.get(id = is_id)

            if not Personel.objects.filter(tcno = tcno):

                yeniPersonel = Personel(ad = ad, soyad = soyad, adres = adres, telefon = telefon, eposta = eposta, tcno = tcno, ehliyet_no = ehliyet_no, kan_grubu = kan_grubu, sgk_no = sgk_no, is_id = mevcutIs)

                yeniPersonel.save()

                return  render(request, "personelEkle.html", { "mevcutIs" : mevcutIs ,"alert" : "Yeni personel başarılı bir şekilde eklendi.", "alertStatus" : True})
            else:
                return render(request, "personelEkle.html",
                              { "mevcutIs" : mevcutIs ,"alert": "Aynı personel ikinci kez eklenemez. TC numarasının değiştirip tekrar deneyin.", "alertStatus": False})
        else:
            return render(request, "personelEkle.html",
                          { "mevcutIs" : mevcutIs ,"alert": "Personel ekleme işlemi başarısız! Tüm alanları doldurup tekrar deneyin.", "alertStatus": False})
    else:
        return  render(request, "personelEkle.html", { "mevcutIs" : mevcutIs })


def personelSil(request, id):

    personel = get_object_or_404(Personel, id = id)

    personel.aktifmi = False

    personel.save()

    return redirect("/personelListe")

def personelBelgeler(request, id):

    personel = get_object_or_404(Personel, id = id)

    belgeler = Belge.objects.filter(personel_id = id)

    return  render(request, "personelBelgeler.html", { "personel" : personel, "belgeler" : belgeler, "mevcutIs" : personel.is_id.id })

def personelDetay(request, id):

    personel = get_object_or_404(Personel, id=id)

    mevcutIs = get_object_or_404(Is, id = personel.is_id.id)

    belgeler = Belge.objects.filter(personel_id=id).filter(aktifmi = True)

    yuklenecekBelgeSayisi = mevcutIs.guvenlik_seviye.id - len(belgeler)

    return render(request, "personelDetay.html", { "personel" : personel, "belgeler" : belgeler, "mevcutIs" : mevcutIs, "yuklenecekBelgeSayisi" : yuklenecekBelgeSayisi })

def belgeListe(request):

    personeller = Personel.objects.filter(is_id = request.session['mevcutIs'])

    belgeler = Belge.objects.filter(aktifmi = True)

    return render(request, "belgeListe.html", { "mevcutIs" : request.session['mevcutIs'], "belgeler" : belgeler, "personeller" : personeller })

def belgeEkle(request, id):

    #personeller = Personel.objects.filter(is_id = request.session['mevcutIs'])

    personel = get_object_or_404(Personel, id = id)

    ad = request.POST.get("ad")
    aciklama = request.POST.get("aciklama")
    #personel_id = request.POST.get("personel")
    personel_id = personel
    belge = request.FILES.get("belge")
    belge_durum = BelgeDurum.objects.get(ad = "Onay Bekliyor")

    if request.POST.get("ekle") :

        #print ("Bilgiler")
        #print (ad)
        #print (aciklama)
        #print (personel_id)
        #print (belge.size)
        #print (belge_durum)

        if ad and aciklama and personel_id and belge :

            if not Belge.objects.filter(belge = belge):

                path = default_storage.save('documents/'+belge.name , ContentFile(belge.read()))

                #personel = Personel.objects.get(id = personel_id)

                belge = Belge(ad = ad, aciklama = aciklama, personel_id = personel_id, belge = path, belge_durum = belge_durum)

                belge.save()

                return render(request, "belgeEkle.html", {"personel" : personel_id, "alert" : "Belge ekleme işlemi başarılı.", "alertStatus" : True})

            else :

                return render(request, "belgeEkle.html", {"personel" : personel_id, "alert" : "Belge ekleme işlemi başarısız! Aynı belgeyi ikinci defa yükleyemezsiniz. Farklı bir belge yükleyerek tekrar deneyin.", "alertStatus" : False})
        else:
            return render(request, "belgeEkle.html",
                          {"personeller": personeller, "alert": "Belge ekleme işlemi başarısız! Tüm alanları doldurup tekrar deneyin.", "alertStatus": False})
    else:
        return render(request, "belgeEkle.html", { "personel" : personel_id })

def belgeSil(request, id):

    belge = get_object_or_404(Belge, id = id)

    belge.aktifmi = False

    belge.save()

    geriDonulecekSayfa = "/{0}/{1}".format("personelDetay" , belge.personel_id.id)

    return redirect(geriDonulecekSayfa)

def belgeOnizle(request, id):

    belge = get_object_or_404(Belge, id = id)

    file_path = belge.belge.path

    print (file_path)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + belge.personel_id.ad + " " + belge.personel_id.soyad + "-" + belge.ad + ".pdf"
            return response
    raise Http404

def belgeOnay(request, id):

    Belge.objects.filter(id = id).update(belge_durum = 3)

    belge = get_object_or_404(Belge, id = id)

    geriDonulecekSayfa = "/{0}/{1}".format("personelBelgeler", belge.personel_id.id)

    return redirect(geriDonulecekSayfa)


def belgeRed(request, id):

    Belge.objects.filter(id = id).update(belge_durum = 4)

    belge = get_object_or_404(Belge, id = id)

    geriDonulecekSayfa = "/{0}/{1}".format("personelBelgeler", belge.personel_id.id)

    return redirect(geriDonulecekSayfa)