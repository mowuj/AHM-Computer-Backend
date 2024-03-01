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


class Cart(models.Model):
    orderId = models.IntegerField()
    customer = models.ForeignKey(
        User, related_name="cart_user", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="cart_product", on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    amount = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)

    def calculate_total_price(self):
        self.amount = self.product.price  
        self.total_amount = self.Quantity * self.amount
        return self.total_amount

    def save(self, *args, **kwargs):

        self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order ID: {self.orderId}, Product: {self.product.name}, Quantity: {self.Quantity}, Total Amount: {self.total_amount}"
