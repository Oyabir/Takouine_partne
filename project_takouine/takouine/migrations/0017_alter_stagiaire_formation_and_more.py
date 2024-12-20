# Generated by Django 5.0.2 on 2024-03-11 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0016_partenaire_achat_alter_stagiaire_formation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stagiaire',
            name='formation',
            field=models.CharField(choices=[('Español', 'Español'), ('English', 'English'), ('Francais', 'Francais'), ('Allemand', 'Allemand')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='stagiaireCode',
            field=models.CharField(default='KT49a890b7', max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Visite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_visited', models.DateField(auto_now_add=True)),
                ('partenaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='takouine.partenaire')),
            ],
            options={
                'verbose_name': 'Visite',
                'verbose_name_plural': 'Visites',
            },
        ),
    ]
