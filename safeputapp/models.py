# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# Firma nesnesini tanımlayan model.
class Firma(models.Model):
    kutuk_no = models.CharField(max_length = 10, verbose_name = "Kütük Numarası")
    unvan = models.CharField(max_length = 50, verbose_name = "Ünvan")
    adres = models.CharField(max_length = 250, verbose_name = "Adres")
    posta_kodu = models.CharField(max_length = 10, verbose_name = "Posta Kodu")
    sehir = models.CharField(max_length = 50, verbose_name = "Şehir")
    telefon = models.CharField(max_length = 20, verbose_name = "Telefon")
    faks = models.CharField(max_length = 20, verbose_name = "Faks")
    eposta = models.CharField(max_length = 50, verbose_name = "E-Posta")
    aktifmi = models.BooleanField(verbose_name = "Aktif mi?", default = True)
    olusturma_tarihi = models.DateTimeField(auto_now_add = True, blank = True, verbose_name = "Oluşturma Tarihi")
    duzunleme_tarihi = models.DateTimeField(verbose_name = "Duzenleme Tarihi", blank = True, null = True)

    def __unicode__(self):
        return self.unvan

# IsDurum nesnesini tanımlayan model.
class IsDurum(models.Model):
    tanim = models.CharField(max_length = 50, verbose_name = "Tanım", null = False, blank = False)

    def __unicode__(self):
        return self.tanim

# Is nesnesini tanımlayan model.
class Is(models.Model):
    ad = models.CharField(max_length = 50, verbose_name = "Ad")
    tanim = models.CharField(max_length = 250, verbose_name = "Tanım")
    fatura_no = models.CharField(max_length = 20, verbose_name = "Fatura Numarası")
    guvenlik_seviye = models.CharField(max_length = 20, verbose_name = "Güvenlik Seviyesi")
    #is_onay = models.BooleanField(verbose_name = "İş Onayı", default = False)
    is_durum = models.ForeignKey(IsDurum, on_delete = models.CASCADE, verbose_name = "Durum")
    aktifmi = models.BooleanField(verbose_name = "Aktif mi?", default = True)
    firma_id = models.ForeignKey(Firma, on_delete = models.CASCADE, verbose_name = "Firma")
    olusturma_tarihi = models.DateTimeField(auto_now_add = True, blank = True, verbose_name = "Oluşturma Tarihi")
    duzunleme_tarihi = models.DateTimeField(verbose_name = "Duzenleme Tarihi", blank = True, null = True)
    baglanti = models.CharField(max_length = 100, verbose_name = "Bağlantı")

    def __unicode__(self):
        return self.ad


# Personel nesnesini tanımlayan model.
class Personel(models.Model):
    ad = models.CharField(max_length = 50, verbose_name = "Ad")
    soyad = models.CharField(max_length = 50, verbose_name = "Soyad")
    adres = models.CharField(max_length = 250, verbose_name = "Adres")
    telefon = models.CharField(max_length = 11, verbose_name = "Telefon")
    eposta = models.CharField(max_length = 50, verbose_name = "E-Posta")
    tcno = models.CharField(max_length = 11, verbose_name = "TC Kimlik Numarası")
    ehliyet_no = models.CharField(max_length = 20, verbose_name = "Ehliyet Numarası")
    kan_grubu = models.CharField(max_length = 10, verbose_name = "Kan Grubu")
    sgk_no = models.CharField(max_length = 250, verbose_name = "SGK Numarası")
    is_id = models.ForeignKey(Is, on_delete = models.CASCADE, verbose_name = "İş")
    aktifmi = models.BooleanField(verbose_name = "Aktif mi?", default = True)
    olusturma_tarihi = models.DateTimeField(auto_now_add = True, blank = True, verbose_name = "Oluşturma Tarihi")
    duzunleme_tarihi = models.DateTimeField(verbose_name = "Duzenleme Tarihi", blank = True, null = True)

    def __unicode__(self):
        return self.ad

# BelgeDurum nesnesini tanimlayan model.
class BelgeDurum(models.Model):
    ad = models.CharField(max_length = 50, verbose_name = "Ad")
    durum = models.CharField(max_length = 20, verbose_name = "Durum")
    aktifmi = models.BooleanField(verbose_name = "Aktif mi?", default = True)
    olusturma_tarihi = models.DateTimeField(auto_now_add = True, blank = True, verbose_name = "Oluşturma Tarihi")
    duzunleme_tarihi = models.DateTimeField(verbose_name = "Duzenleme Tarihi", blank = True, null = True)

    def __unicode__(self):
        return self.ad

# Belge nesnesini tanımlayan model.
class Belge(models.Model):
    ad = models.CharField(max_length = 50, verbose_name = "Ad")
    aciklama = models.CharField(max_length = 50, verbose_name = "Açıklama")
    personel_id = models.ForeignKey(Personel, on_delete = models.CASCADE, verbose_name = "Personel")
    belge = models.FileField(upload_to='documents/')
    belge_durum = models.ForeignKey(BelgeDurum, on_delete = models.CASCADE, verbose_name = "Belge Durum")
    aktifmi = models.BooleanField(verbose_name = "Aktif mi?", default = True)
    olusturma_tarihi = models.DateTimeField(auto_now_add = True, blank = True, verbose_name = "Oluşturma Tarihi")
    duzunleme_tarihi = models.DateTimeField(verbose_name = "Duzenleme Tarihi", blank = True, null = True)

    def __unicode__(self):
        return self.ad


# Eposta nesnesini tanımlayan model.
class Eposta(models.Model):
    baslik = models.CharField(max_length = 50, verbose_name = "Başlık")
    mesaj = models.CharField(max_length = 1000, verbose_name = "Mesaj")
    is_id = models.ForeignKey(Is, on_delete = models.CASCADE, verbose_name = "İş")
    baglanti_link = models.CharField(max_length = 100, verbose_name = "Bağlantı Linki")
    aktifmi = models.BooleanField(verbose_name = "Aktif mi?", default = True)
    olusturma_tarihi = models.DateTimeField(auto_now_add = True, blank = True, verbose_name = "Oluşturma Tarihi")
    duzunleme_tarihi = models.DateTimeField(verbose_name = "Duzenleme Tarihi", blank = True, null = True)

    def __unicode__(self):
        return self.baslik


# Kullanici nesnesini tanımlayan model.
class Kullanici(models.Model):
    ad = models.CharField(max_length = 50, verbose_name = "Ad", null = False, blank = False)
    sifre = models.CharField(max_length = 50, verbose_name = "Şifre", null = False, blank = False)

    def __unicode__(self):
        return self.ad