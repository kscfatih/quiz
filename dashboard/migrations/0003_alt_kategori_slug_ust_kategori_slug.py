# Generated by Django 4.2.4 on 2023-09-25 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_ust_kategori_alt_kategori'),
    ]

    operations = [
        migrations.AddField(
            model_name='alt_kategori',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AddField(
            model_name='ust_kategori',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]