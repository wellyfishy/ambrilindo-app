# Generated by Django 4.1.7 on 2023-09-06 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bagan', '0010_alter_atlet_jenis_kelamin'),
    ]

    operations = [
        migrations.AddField(
            model_name='bagankategori',
            name='tatami_nomor_tanding',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bagan.tatami'),
        ),
    ]
