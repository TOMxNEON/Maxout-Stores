# Generated by Django 4.1.6 on 2023-03-06 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_cartitem_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='customer',
        ),
    ]
