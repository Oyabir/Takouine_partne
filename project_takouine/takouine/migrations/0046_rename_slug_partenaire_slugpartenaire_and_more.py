# Generated by Django 5.0.2 on 2024-04-02 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0045_stagiaire_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partenaire',
            old_name='slug',
            new_name='slugPartenaire',
        ),
        migrations.RenameField(
            model_name='stagiaire',
            old_name='slug',
            new_name='slugStagiaire',
        ),
    ]