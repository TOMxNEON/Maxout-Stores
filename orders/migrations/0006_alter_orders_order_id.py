# Generated by Django 4.1.6 on 2023-03-13 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_orders_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_id',
            field=models.CharField(default='0BDB719A', max_length=8),
        ),
    ]
