# Generated by Django 4.1.6 on 2023-03-08 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='order_number',
        ),
        migrations.AlterField(
            model_name='orders',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('Razorpay', 'Razorpay'), ('COD', 'COD')], max_length=30, null=True),
        ),
    ]
