# Generated by Django 4.2.4 on 2023-10-01 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0028_cekilis_cekilis_verileri'),
    ]

    operations = [
        migrations.AddField(
            model_name='cekilis',
            name='alanlar',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Cekilis_verileri',
        ),
    ]
