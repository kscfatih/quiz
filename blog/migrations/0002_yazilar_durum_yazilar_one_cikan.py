# Generated by Django 4.2.4 on 2023-10-12 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='yazilar',
            name='durum',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='yazilar',
            name='one_cikan',
            field=models.TextField(blank=True, null=True),
        ),
    ]