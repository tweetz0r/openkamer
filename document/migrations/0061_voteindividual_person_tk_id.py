# Generated by Django 2.2.8 on 2019-12-08 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0060_auto_20191129_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='voteindividual',
            name='person_tk_id',
            field=models.CharField(blank=True, db_index=True, max_length=200),
        ),
    ]
