# Generated by Django 4.1 on 2022-08-27 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcomApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_off',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
