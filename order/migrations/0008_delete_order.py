# Generated by Django 4.2 on 2024-03-06 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_remove_order_cart'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
