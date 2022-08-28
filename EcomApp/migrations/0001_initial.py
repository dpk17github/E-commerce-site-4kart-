# Generated by Django 4.1 on 2022-08-27 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('price', models.IntegerField(default=0)),
                ('des', models.CharField(max_length=300)),
                ('img', models.ImageField(default='', upload_to='static/img')),
            ],
        ),
    ]
