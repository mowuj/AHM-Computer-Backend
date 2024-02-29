from django.shortcuts import render
from . import models
from . import serializers
from rest_framework import viewsets, status
from rest_framework.response import Response

class CategoryViewset(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class BrandViewset(viewsets.ModelViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer

class ProductViewset(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ReviewViewset(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer


class CartViewset(viewsets.ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer

    def create(self, request, *args, **kwargs):
        request.data['customer'] = request.user.id

        last_order = models.Cart.objects.order_by('-orderId').first()
        if last_order:
            request.data['orderId'] = last_order.orderId + 1
        else:
            request.data['orderId'] = 10001
        quantity = request.data.get('Quantity', 1)
        product = request.data.get('product')

        if product:
            product_instance = models.Product.objects.get(pk=product)

            amount_per_item = product_instance.price
            request.data['amount'] = amount_per_item * quantity
        else:
            request.data['amount'] = 0

        request.data['total_amount'] = request.data['amount'] * quantity

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
