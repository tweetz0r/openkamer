# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-19 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('government', '0003_auto_20161019_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='governmentmember',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
