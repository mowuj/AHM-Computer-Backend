# Generated by Django 4.2 on 2024-03-10 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_remove_order_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='subtotal',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='payment_completed',
        ),
    ]