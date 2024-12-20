# Generated by Django 5.0.2 on 2024-03-13 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0019_visite_stagiaire_alter_stagiaire_stagiairecode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achat',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='formation',
            field=models.CharField(choices=[('Francais', 'Francais'), ('Allemand', 'Allemand'), ('English', 'English'), ('Español', 'Español')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='stagiaireCode',
            field=models.CharField(default='KTfc89f4fe', max_length=100, null=True),
        ),
    ]
