# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-08 13:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0038_auto_20170308_1120'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kamervraag',
            options={'ordering': ['-document__date_published']},
        ),
    ]
