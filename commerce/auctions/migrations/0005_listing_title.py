# Generated by Django 4.1.7 on 2023-04-12 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_listing_categories_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='title',
            field=models.CharField(default='Default title', max_length=64),
        ),
    ]
