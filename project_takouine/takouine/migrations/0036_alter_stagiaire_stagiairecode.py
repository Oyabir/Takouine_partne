# Generated by Django 5.0.2 on 2024-03-21 15:29

import takouine.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0035_formation_date_created_alter_stagiaire_stagiairecode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stagiaire',
            name='stagiaireCode',
            field=models.CharField(default=takouine.models.generate_stagiaire_code, max_length=100, null=True),
        ),
    ]
