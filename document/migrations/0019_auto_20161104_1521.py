# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-04 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0018_auto_20161104_1412'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='', max_length=250),
        ),
    ]