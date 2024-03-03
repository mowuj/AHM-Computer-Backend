from django.db import models
from django.contrib.auth.models import User
from cart.models import Cart
from customer.models import Customer
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
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=250)
    phone = models.CharField(max_length=13)
    email = models.EmailField(null=True, blank=True)
    shipping_address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=250, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=20, choices=METHOD, default="Cash On Delivery")
    payment_completed = models.BooleanField(
        default=False, null=True, blank=True)

    def __str__(self):
        return "Order: " + str(self.id)
