# Generated by Django 5.0.2 on 2024-03-11 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0014_alter_stagiaire_formation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partenaire',
            name='Achat',
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='formation',
            field=models.CharField(choices=[('Francais', 'Francais'), ('Allemand', 'Allemand'), ('English', 'English'), ('Español', 'Español')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='stagiaireCode',
            field=models.CharField(default='KTe31343e9', max_length=100, null=True),
        ),
    ]
