# Generated by Django 4.2 on 2024-03-02 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_order_cart'),
        ('product', '0002_remove_cart_orderid_cart_cartid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
