# Generated by Django 4.2 on 2024-03-02 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_remove_order_quantity_remove_order_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
    ]