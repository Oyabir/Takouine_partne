# Generated by Django 5.0.2 on 2024-03-13 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0030_rename_date_purchased_achat_date_added_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stagiaire',
            name='formation',
            field=models.CharField(choices=[('Español', 'Español'), ('Francais', 'Francais'), ('Allemand', 'Allemand'), ('English', 'English')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='stagiaireCode',
            field=models.CharField(default='KT92cf0545', max_length=100, null=True),
        ),
    ]
