# Generated by Django 4.2.3 on 2023-09-21 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0013_testler_yanlis_soru'),
    ]

    operations = [
        migrations.AddField(
            model_name='testler',
            name='alanlar',
            field=models.TextField(blank=True, null=True),
        ),
    ]
