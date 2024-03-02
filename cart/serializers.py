from rest_framework import serializers
from . models import Cart,CartProduct
from django.contrib.auth.models import User

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['customer','total']

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = '__all__'
