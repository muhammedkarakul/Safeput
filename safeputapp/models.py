# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# Firma nesnesini tanımlayan model.
class Firma(models.Model):
    kutuk_no = models.CharField(max_lenght = 9, verbose_name = "Kütük Numarası")
    unvan = models.CharField(max_lenght = 50, verbose_name = "Ünvan")
    adres = models.CharField(max_lenght = 250, verbose_name = "Adres")
    posta_kodu = models.CharField(max_lenght = 5, verbose_name = "Posta Kodu")
    sehir = models.CharField(max_lenght = 20, verbose_name = "Şehir")
    telefon = models.CharField(max_lenght = 11, verbose_name = "Telefon")
    faks = models.CharField(max_lenght = 11, verbose_name = "Faks")
    eposta = models.CharField(max_lenght = 50, verbose_name = "E-Posta")
    aktifmi = models.BooleanField(verbose_name = "Aktif mi?", default = True)
    olusturma_tarihi = models.DateTimeField(verbose_name = "Oluşturma Tarihi")
    duzunleme_tarihi = models.DateTimeField(verbose_name = "Duzenleme Tarihi", blank = True, null = True)


# İş nesnesini tanımlayan model.
class Is(models.Model):
    tanim = models.CharField(max_lenght = 250, verbose_name = "Tanım")
    fatura_no = models.CharField(max_lenght = 20, verbose_name = "Fatura Numarası")
    guvenlik_seviye = models.CharField(max_lenght = 20, verbose_name = "Güvenlik Seviyesi")
    is_durum = models.CharField(max_lenght = 20, verbose_name = "İş Durumu")
    aktifmi = models.BooleanField(verbose_name = "Aktif mi?", default = True)
    firma_id = models.CharField(max_lenght = 10, verbose_name = "Firma ID")
    olusturma_tarihi = models.DateTimeField(verbose_name = "Oluşturma Tarihi")
    duzunleme_tarihi = models.DateTimeField(verbose_name = "Duzenleme Tarihi", blank = True, null = True)


# Personel nesnesini tanımlayan model.
class Personel(models.Model):
    ad = models.CharField(max_lenght = 50, verbose_name = "Ad")
    soyad = models.CharField(max_lenght = 50, verbose_name = "Soyad")
    adres = models.CharField(max_lenght = 250, verbose_name = "Adres")
    telefon = models.CharField(max_lenght = 11, verbose_name = "Telefon")
    eposta = models.CharField(max_lenght = 50, verbose_name = "E-Posta")
    tcno = models.CharField(max_lenght = 11, verbose_name = "TC Kimlik Numarası")
    ehliyet_no = models.CharField(max_lenght = 20, verbose_name = "Ehliyet Numarası")
    kan_grubu = models.CharField(max_lenght = 10, verbose_name = "Kan Grubu")
    sgk_no = models.CharField(max_lenght = 250, verbose_name = "SGK Numarası")
    is_id = models.CharField(max_lenght = 250, verbose_name = "İş ID")

# Belge nesnesini tanımlayan model.
class Belge(models.Model):


# BelgeDurum nesnesini tanimlayan model.
class BelgeDurum(models.Model):






