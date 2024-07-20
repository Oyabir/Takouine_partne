# Generated by Django 5.0.2 on 2024-03-13 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0024_alter_achat_date_added_alter_stagiaire_formation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achat',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='formation',
            field=models.CharField(choices=[('Allemand', 'Allemand'), ('Español', 'Español'), ('Francais', 'Francais'), ('English', 'English')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='stagiaireCode',
            field=models.CharField(default='KTac7be517', max_length=100, null=True),
        ),
    ]