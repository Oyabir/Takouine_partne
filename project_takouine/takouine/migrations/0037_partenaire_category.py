# Generated by Django 5.0.2 on 2024-03-26 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0036_alter_stagiaire_stagiairecode'),
    ]

    operations = [
        migrations.AddField(
            model_name='partenaire',
            name='category',
            field=models.CharField(choices=[('Telephone et tablette', 'Telephone et tablette'), ('Electromenager', 'Electromenager'), ('Informatique', 'Informatique'), ('Maison et cuisine', 'Maison et cuisine'), ('Bureau', 'Bureau'), ('Vetements et chaussures', 'Vetements et chaussures'), ('Beautes et sante', 'Beautes et sante'), ('Jeux Videos et consoles', 'Jeux Videos et consoles'), ('Sport et Loisirs', 'Sport et Loisirs'), ('Bebe et Jouets', 'Bebe et Jouets'), ('Supermarche', 'Supermarche'), ('Librairies', 'Librairies'), ('Services', 'Services')], max_length=50, null=True),
        ),
    ]
