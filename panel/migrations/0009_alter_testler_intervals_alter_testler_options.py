# Generated by Django 4.2.4 on 2023-09-14 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0008_remove_testler_question_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testler',
            name='intervals',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='testler',
            name='options',
            field=models.JSONField(blank=True, null=True),
        ),
    ]