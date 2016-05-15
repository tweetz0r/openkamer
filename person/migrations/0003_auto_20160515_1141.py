# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-15 09:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_person_wikimedia_image_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='wikimedia_image_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='surname_prefix',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
