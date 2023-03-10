# Generated by Django 4.1.6 on 2023-03-07 05:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '__first__'),
        ('store', '0016_cart_customer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20)),
                ('oder_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('payment_method', models.CharField(blank=True, choices=[('razorpay', 'razorpay'), ('COD', 'COD')], max_length=30, null=True)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('OrderPending', 'Orderpending'), ('Packed', 'Packed'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned')], default='Orderpending', max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True, null=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.cart')),
                ('cartitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.cartitem')),
                ('delivery_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.addresses')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.variants')),
            ],
        ),
    ]
