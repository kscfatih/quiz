# Generated by Django 4.2.4 on 2023-10-14 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_bize_ulasin'),
    ]

    operations = [
        migrations.AddField(
            model_name='bize_ulasin',
            name='tarih',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
