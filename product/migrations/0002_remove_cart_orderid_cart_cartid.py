# Generated by Django 4.2 on 2024-03-01 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='orderId',
        ),
        migrations.AddField(
            model_name='cart',
            name='cartId',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
