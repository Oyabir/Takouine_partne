# Generated by Django 5.0.2 on 2024-03-08 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0010_rename_date_début_stagiaire_date_debut_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stagiaire',
            name='formation',
            field=models.CharField(choices=[('English', 'English'), ('Francais', 'Francais'), ('Allemand', 'Allemand'), ('Español', 'Español')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='stagiaireCode',
            field=models.CharField(default='KT7ba38dfb', max_length=100, null=True),
        ),
    ]
