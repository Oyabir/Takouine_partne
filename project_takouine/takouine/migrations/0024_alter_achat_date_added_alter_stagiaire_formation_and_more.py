# Generated by Django 5.0.2 on 2024-03-13 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0023_alter_achat_date_added_alter_stagiaire_formation_and_more'),
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
            field=models.CharField(choices=[('English', 'English'), ('Francais', 'Francais'), ('Allemand', 'Allemand'), ('Español', 'Español')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='stagiaireCode',
            field=models.CharField(default='KT6d5ceac5', max_length=100, null=True),
        ),
    ]
