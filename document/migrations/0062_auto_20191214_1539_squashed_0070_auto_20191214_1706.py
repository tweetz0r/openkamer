# Generated by Django 2.2.8 on 2019-12-14 17:03

from django.db import migrations, models
import django.db.models.deletion
import tkapi.besluit


class Migration(migrations.Migration):

    replaces = [('document', '0062_auto_20191214_1539'), ('document', '0063_auto_20191214_1613'), ('document', '0064_decision_date'), ('document', '0065_auto_20191214_1644'), ('document', '0066_decision_kamerstuk'), ('document', '0067_auto_20191214_1655'), ('document', '0068_auto_20191214_1701'), ('document', '0069_auto_20191214_1704'), ('document', '0070_auto_20191214_1706')]

    dependencies = [
        ('document', '0061_voteindividual_person_tk_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='besluititem',
            name='besluiten_lijst',
        ),
        migrations.RemoveField(
            model_name='besluititemcase',
            name='besluit_item',
        ),
        migrations.DeleteModel(
            name='BesluitenLijst',
        ),
        migrations.DeleteModel(
            name='BesluitItem',
        ),
        migrations.DeleteModel(
            name='BesluitItemCase',
        ),
        migrations.RenameField(
            model_name='dossier',
            old_name='decision',
            new_name='decision_text',
        ),
        migrations.AddField(
            model_name='voting',
            name='tk_id',
            field=models.CharField(blank=True, db_index=True, max_length=200),
        ),
        migrations.CreateModel(
            name='Decision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tk_id', models.CharField(blank=True, db_index=True, max_length=200)),
                ('status', models.CharField(choices=[(tkapi.besluit.BesluitStatus('Besluit'), 'Besluit'), (tkapi.besluit.BesluitStatus('Concept voorstel'), 'Concept voorstel'), (tkapi.besluit.BesluitStatus('Voorstel'), 'Voorstel'), (tkapi.besluit.BesluitStatus('Nog te verwerken besluit'), 'Nog te verwerken besluit')], db_index=True, max_length=200)),
                ('text', models.CharField(blank=True, max_length=10000)),
                ('type', models.CharField(blank=True, max_length=10000)),
                ('note', models.CharField(blank=True, max_length=10000)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('dossier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='document.Dossier')),
                ('datetime', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('kamerstuk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='document.Kamerstuk')),
            ],
        ),
        migrations.AddField(
            model_name='voting',
            name='decision',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='document.Decision'),
        ),
        migrations.AlterField(
            model_name='document',
            name='date_published',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='date_published',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='datetime',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]