from django.db import models
from django.contrib.auth.models import User
from cart.models import Cart
from customer.models import Customer
from product.models import Product
from payment .models import Payment
# Create your models here.

ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Canceled"),
)
METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Stripe", "Stripe")
)


class Order(models.Model):
    ordered_by = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_amount = models.PositiveIntegerField(default=0)
    order_status = models.CharField(
        max_length=250, choices=ORDER_STATUS, default="Order Received")
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True)
    payment_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('order', 'product')



class Shipment(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=250)
    phone = models.CharField(max_length=13)
    email = models.EmailField(null=True, blank=True)
    shipping_address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    total = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=20, choices=METHOD, default="Cash On Delivery")
    def __str__(self):
        return "Order: " + str(self.id)
