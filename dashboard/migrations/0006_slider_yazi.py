# Generated by Django 4.2.4 on 2023-09-26 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_site_ayar_hakkimizda_resim'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='yazi',
            field=models.TextField(blank=True, null=True),
        ),
    ]