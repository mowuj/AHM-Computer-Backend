from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Details(models.Model):
    user = models.ForeignKey(
        User, related_name="details", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=11)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=200)
    landmark=models.CharField(max_length=200)
    postcode = models.CharField(max_length=50)
    city = models.CharField(max_length=150)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
