# Generated by Django 5.0.2 on 2024-04-09 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0051_formation_slugformation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formation',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
