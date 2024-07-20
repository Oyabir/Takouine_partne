# Generated by Django 5.0.2 on 2024-03-13 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0026_alter_stagiaire_formation_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='achat',
            old_name='date_added',
            new_name='date_purchased',
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='formation',
            field=models.CharField(choices=[('Allemand', 'Allemand'), ('Español', 'Español'), ('Francais', 'Francais'), ('English', 'English')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='stagiaireCode',
            field=models.CharField(default='KT28c9967d', max_length=100, null=True),
        ),
    ]
