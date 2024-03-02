from django.db import models
from django.contrib.auth.models import User
from .constants import RATING
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    category = models.ManyToManyField(Category)
    brand = models.ManyToManyField(Brand)
    image = models.ImageField(
        default='default.jpg', upload_to='media/images')
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    discount=models.PositiveIntegerField(null=True,default=0)
    def __str__(self):
        return f"name: {self.name}, category: {self.category}, brand: {self.brand}"



class Review(models.Model):
    customer = models.ForeignKey(
        User, related_name="reviews", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING)
    body = models.TextField()
    models.DateTimeField(auto_now_add=True)
    timestamps = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

