# Generated by Django 4.1.6 on 2023-03-04 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_remove_variants_variant_color_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='product_var',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='store.products'),
            preserve_default=False,
        ),
    ]
