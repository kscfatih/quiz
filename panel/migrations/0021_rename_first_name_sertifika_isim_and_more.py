# Generated by Django 4.2.4 on 2023-09-24 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0020_sertifika'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sertifika',
            old_name='first_name',
            new_name='isim',
        ),
        migrations.RemoveField(
            model_name='sertifika',
            name='last_name',
        ),
    ]
