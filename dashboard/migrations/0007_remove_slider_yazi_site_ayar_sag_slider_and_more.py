# Generated by Django 4.2.4 on 2023-09-27 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_slider_yazi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slider',
            name='yazi',
        ),
        migrations.AddField(
            model_name='site_ayar',
            name='sag_slider',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='site_ayar',
            name='sol_slider',
            field=models.TextField(blank=True, null=True),
        ),
    ]
