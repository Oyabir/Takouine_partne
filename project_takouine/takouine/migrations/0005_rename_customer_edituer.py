# Generated by Django 5.0.2 on 2024-03-01 15:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0004_stagiaire'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Customer',
            new_name='Edituer',
        ),
    ]
