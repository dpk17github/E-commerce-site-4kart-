# Generated by Django 4.1 on 2022-08-28 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcomApp', '0002_product_price_off_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='search_key',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
    ]
