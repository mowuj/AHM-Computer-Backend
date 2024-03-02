from django.shortcuts import render
from . import models
from . import serializers 
# Create your views here.
from rest_framework import viewsets

class CartViewset(viewsets.ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer

class CartProductViewset(viewsets.ModelViewSet):
    queryset = models.CartProduct.objects.all()
    serializer_class = serializers.CartProductSerializer
