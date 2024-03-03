from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Order(models.Model):
    customer = models.ForeignKey(
        User, related_name="orders", on_delete=models.CASCADE)

    total_amount = models.IntegerField()

    def __str__(self):
        return self.orderId
