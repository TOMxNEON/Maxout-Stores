# Generated by Django 4.1.6 on 2023-02-20 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_account_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_photos/default.png', null=True, upload_to='profile_photos/'),
        ),
    ]