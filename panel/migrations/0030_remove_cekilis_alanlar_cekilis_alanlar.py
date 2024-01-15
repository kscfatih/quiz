# Generated by Django 4.2.4 on 2023-10-01 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0029_cekilis_alanlar_delete_cekilis_verileri'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cekilis',
            name='alanlar',
        ),
        migrations.CreateModel(
            name='Cekilis_alanlar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_soyad', models.TextField(blank=True, null=True)),
                ('sinif', models.TextField(blank=True, null=True)),
                ('okul', models.TextField(blank=True, null=True)),
                ('urun', models.TextField(blank=True, null=True)),
                ('resim', models.TextField(blank=True, null=True)),
                ('aciklama', models.TextField(blank=True, null=True)),
                ('cekilis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='panel.cekilis')),
            ],
        ),
    ]