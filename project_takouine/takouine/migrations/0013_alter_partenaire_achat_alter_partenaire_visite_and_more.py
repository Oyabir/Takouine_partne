# Generated by Django 5.0.2 on 2024-03-09 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0012_partenaire_achat_partenaire_visite_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partenaire',
            name='Achat',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='partenaire',
            name='Visite',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='stagiaireCode',
            field=models.CharField(default='KT2afd3a4b', max_length=100, null=True),
        ),
    ]