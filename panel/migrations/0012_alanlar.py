# Generated by Django 4.2.4 on 2023-09-20 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0011_testler_kullanici_formu'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alanlar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('type', models.TextField(blank=True, null=True)),
                ('slug', models.TextField(blank=True, null=True)),
                ('options', models.TextField(blank=True, null=True)),
                ('published', models.TextField(blank=True, null=True)),
                ('attr_options', models.TextField(blank=True, null=True)),
                ('author_id', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
