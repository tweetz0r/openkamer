# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('government', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='government',
            name='date_dissolved',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='government',
            name='date_formed',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='governmentmember',
            name='end_date',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='governmentmember',
            name='start_date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='governmentposition',
            name='position',
            field=models.CharField(choices=[('MIN', 'Minister'), ('MWP', 'Minister zonder portefeuille'), ('SOS', 'Staatssecretaris'), ('PMI', 'Minister-president'), ('DPM', 'Viceminister-president')], db_index=True, max_length=3),
        ),
    ]
