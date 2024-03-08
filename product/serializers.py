from rest_framework import serializers
from . models import Product, Category, Brand, Review
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['slug']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ['slug']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'



