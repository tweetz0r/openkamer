# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 13:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0018_auto_20161127_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='besluititemcase',
            name='related_commissions',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='besluititemcase',
            name='related_document_ids',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='dossier',
            name='decision',
            field=models.CharField(blank=True, max_length=2000),
        ),
    ]
