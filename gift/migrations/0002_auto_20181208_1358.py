# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-08 12:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('government', '0003_auto_20161226_1012'),
        ('person', '0005_person_twitter_username'),
        ('parliament', '0006_auto_20170327_0914'),
        ('gift', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('government_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='government.GovernmentMember')),
                ('parliament_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='parliament.ParliamentMember')),
                ('party', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='parliament.PoliticalParty')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.Person')),
            ],
        ),
        migrations.AddField(
            model_name='gift',
            name='person_position',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='gift.PersonPosition'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='personposition',
            unique_together=set([('person', 'date')]),
        ),
    ]