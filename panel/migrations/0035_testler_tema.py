# Generated by Django 4.2.4 on 2023-11-06 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0034_testler_cekilis_mesaji'),
    ]

    operations = [
        migrations.AddField(
            model_name='testler',
            name='tema',
            field=models.TextField(blank=True, null=True),
        ),
    ]
