# Generated by Django 5.0.2 on 2024-03-27 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0039_partenaire_address_partenaire_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partenaire',
            name='phone',
        ),
    ]