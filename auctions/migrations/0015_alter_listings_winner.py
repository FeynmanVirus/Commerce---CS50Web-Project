# Generated by Django 4.2.3 on 2023-08-22 10:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_listings_winner_alter_listings_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='winner',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to=settings.AUTH_USER_MODEL, verbose_name='winner'),
        ),
    ]
