# Generated by Django 2.2.8 on 2019-12-14 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0065_auto_20191214_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='decision',
            name='kamerstuk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='document.Kamerstuk'),
        ),
    ]
