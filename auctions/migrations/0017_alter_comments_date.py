# Generated by Django 4.2.3 on 2023-08-22 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_comments_date_alter_listings_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='date',
            field=models.DateField(default='2023-8-22'),
        ),
    ]