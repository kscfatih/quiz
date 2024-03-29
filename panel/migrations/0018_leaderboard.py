# Generated by Django 4.2.4 on 2023-09-23 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0017_rename_fileds_sonuclar_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fields', models.JSONField(blank=True, null=True)),
                ('score', models.TextField(blank=True, null=True)),
                ('ip_adress', models.TextField(blank=True, null=True)),
                ('duration', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('dogru', models.TextField(blank=True, null=True)),
                ('yanlis', models.TextField(blank=True, null=True)),
                ('unique_id', models.TextField(blank=True, null=True)),
                ('quiz', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_leaderboard', to='panel.testler')),
            ],
        ),
    ]
