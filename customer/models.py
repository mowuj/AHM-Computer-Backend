from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(
        User, related_name="profile", on_delete=models.CASCADE,unique=True)
    image = models.ImageField(
        upload_to='customer/images/', blank=True, null=True)
    mobile_no = models.CharField(max_length=11)
    address = models.CharField(max_length=200, blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return self.user.username
