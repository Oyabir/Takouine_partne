# Generated by Django 5.0.2 on 2024-03-08 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0006_partenaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='stagiaire',
            name='avatar',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='stagiaire',
            name='date_début',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='stagiaire',
            name='date_fin',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='stagiaire',
            name='formation',
            field=models.CharField(choices=[('English', 'English'), ('Español', 'Español'), ('Allemand', 'Allemand'), ('Francais', 'Francais')], max_length=200, null=True),
        ),
    ]
