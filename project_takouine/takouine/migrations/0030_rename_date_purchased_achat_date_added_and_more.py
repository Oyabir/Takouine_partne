# Generated by Django 5.0.2 on 2024-03-13 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0029_rename_date_added_achat_date_purchased_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='achat',
            old_name='date_purchased',
            new_name='date_added',
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='formation',
            field=models.CharField(choices=[('English', 'English'), ('Español', 'Español'), ('Francais', 'Francais'), ('Allemand', 'Allemand')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='stagiaire',
            name='stagiaireCode',
            field=models.CharField(default='KT8dca38d5', max_length=100, null=True),
        ),
    ]
