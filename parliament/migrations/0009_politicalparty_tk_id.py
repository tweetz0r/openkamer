# Generated by Django 2.2.8 on 2019-12-14 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0008_commissie'),
    ]

    operations = [
        migrations.AddField(
            model_name='politicalparty',
            name='tk_id',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
    ]
