# Generated by Django 4.2.4 on 2023-09-25 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alt_kategori_slug_ust_kategori_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='slider',
            old_name='baslik',
            new_name='tip',
        ),
    ]
