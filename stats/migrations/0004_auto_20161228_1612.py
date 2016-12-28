# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_partyvotebehaviour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partyvotebehaviour',
            name='voting_type',
            field=models.CharField(blank=True, choices=[('BILL', 'Wetsvoorstel'), ('OTHER', 'Overig (Motie, Amendement)')], max_length=5, null=True),
        ),
    ]
