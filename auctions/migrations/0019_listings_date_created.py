# Generated by Django 4.2.3 on 2023-08-22 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_alter_listings_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='date_created',
            field=models.DateField(default='2023-8-22'),
        ),
    ]
