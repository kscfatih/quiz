# Generated by Django 4.2.4 on 2023-10-12 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_yazilar_durum_yazilar_one_cikan'),
    ]

    operations = [
        migrations.AddField(
            model_name='yazilar',
            name='resim',
            field=models.TextField(blank=True, null=True),
        ),
    ]