# Generated by Django 4.2 on 2024-03-03 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_order_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='orderId',
        ),
    ]
