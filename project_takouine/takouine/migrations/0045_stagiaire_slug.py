# Generated by Django 5.0.2 on 2024-04-02 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0044_contactmessagepartenaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='stagiaire',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
