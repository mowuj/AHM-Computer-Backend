from django.db import models
from django.contrib.auth.models import User

from product.models import Cart

# Create your models here.


class Order(models.Model):
    orderId = models.IntegerField(null=True, blank=True)
    customer = models.ForeignKey(
        User, related_name="orders", on_delete=models.CASCADE)
    cart = models.ForeignKey(
        Cart, related_name="cart", on_delete=models.CASCADE,null=True,blank=True)
    total_amount = models.IntegerField()

    def __str__(self):
        return self.orderId
