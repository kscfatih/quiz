# Generated by Django 4.2.4 on 2023-09-22 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0015_sonuclar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sonuclar',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='sonuclar',
            name='start_date',
        ),
        migrations.AddField(
            model_name='sonuclar',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
