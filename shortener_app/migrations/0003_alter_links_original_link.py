# Generated by Django 5.0.3 on 2024-03-18 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener_app', '0002_alter_links_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='links',
            name='original_link',
            field=models.URLField(max_length=500, unique=True),
        ),
    ]