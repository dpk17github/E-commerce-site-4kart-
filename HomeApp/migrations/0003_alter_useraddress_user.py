# Generated by Django 4.0.4 on 2022-09-02 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('HomeApp', '0002_rename_country_useraddress_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userAddress', to=settings.AUTH_USER_MODEL),
        ),
    ]
