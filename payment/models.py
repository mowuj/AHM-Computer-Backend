from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer
# Create your models here.


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_customer_id = models.CharField(max_length=100,null=True,blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.amount} INR - {self.payment_date}"
