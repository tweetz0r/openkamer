# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-04 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0017_auto_20161102_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='document',
            name='category',
        ),
        migrations.AddField(
            model_name='document',
            name='categories',
            field=models.ManyToManyField(blank=True, to='document.Category'),
        ),
    ]