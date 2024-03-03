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

    def create(self, request, *args, **kwargs):
        cart_id = request.data.get('cart')
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        existing_cart_product = models.CartProduct.objects.filter(
            cart=cart_id, product=product_id).first()

        if existing_cart_product:

            existing_cart_product.quantity += quantity
            existing_cart_product.subtotal = existing_cart_product.price * \
                existing_cart_product.quantity
            existing_cart_product.save()
        else:

            return super().create(request, *args, **kwargs)
