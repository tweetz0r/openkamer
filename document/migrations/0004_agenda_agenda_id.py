# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-17 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0003_agenda_agendaitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenda',
            name='agenda_id',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]