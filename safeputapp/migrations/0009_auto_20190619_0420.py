# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-06-19 01:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('safeputapp', '0008_auto_20190619_0316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='is',
            name='guvenlik_seviye',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='safeputapp.GuvenlikSeviye', verbose_name='G\xfcvenlik Seviyesi'),
        ),
    ]
