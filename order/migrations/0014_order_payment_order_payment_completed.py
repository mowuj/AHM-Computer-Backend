# Generated by Django 4.2 on 2024-03-10 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_payment_delete_details'),
        ('order', '0013_remove_orderproduct_subtotal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_completed',
            field=models.BooleanField(default=False),
        ),
    ]
