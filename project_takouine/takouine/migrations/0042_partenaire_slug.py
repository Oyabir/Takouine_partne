# Generated by Django 5.0.2 on 2024-03-30 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0041_partenaire_companyemail'),
    ]

    operations = [
        migrations.AddField(
            model_name='partenaire',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
