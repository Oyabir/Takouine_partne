# Generated by Django 5.0.2 on 2024-04-04 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takouine', '0049_remove_edituer_slugedituer'),
    ]

    operations = [
        migrations.AddField(
            model_name='edituer',
            name='slugEdituer',
            field=models.SlugField(blank=True, null=True),
        ),
    ]