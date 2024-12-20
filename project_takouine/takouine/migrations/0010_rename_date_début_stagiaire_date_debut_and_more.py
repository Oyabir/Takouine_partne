# Generated by Django 5.0.2 on 2024-03-08 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0009_alter_stagiaire_formation_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stagiaire',
            old_name='date_début',
            new_name='date_debut',
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='formation',
            field=models.CharField(choices=[('Español', 'Español'), ('Allemand', 'Allemand'), ('English', 'English'), ('Francais', 'Francais')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='stagiaireCode',
            field=models.CharField(default='KTc13bc88e', max_length=100, null=True),
        ),
    ]
