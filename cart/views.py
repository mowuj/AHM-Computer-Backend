from django.shortcuts import render
from . import models
from . import serializers
# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

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

        try:
            with transaction.atomic():
                existing_cart_product = models.CartProduct.objects.filter(
                    cart=cart_id, product=product_id).first()

                if existing_cart_product:
                    existing_cart_product.quantity += quantity
                    existing_cart_product.subtotal = existing_cart_product.price * \
                        existing_cart_product.quantity
                    existing_cart_product.save()
                else:
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)

                if request.data.get('order_now'):
                    # Calculate total amount based on existing cart products
                    cart_products = models.CartProduct.objects.filter(
                        cart=cart_id)
                    total_amount = sum(
                        cart_product.subtotal for cart_product in cart_products)

                    order_data = {
                        "cart": cart_id,
                        "ordered_by": request.data.get('ordered_by'),
                        "total_amount": total_amount,
                        "order_status": request.data.get('order_status'),
                        # ... other fields for order details
                    }

                    order_serializer = serializers.OrderSerializer(
                        data=order_data)
                    if order_serializer.is_valid():
                        order_instance = order_serializer.save()

                        for cart_product in cart_products:
                            order_product_data = {
                                "order": order_instance.id,
                                "product": cart_product.product.id,
                                "price": cart_product.price,
                                "quantity": cart_product.quantity,
                                "subtotal": cart_product.subtotal,
                            }
                            order_product_serializer = serializers.OrderProductSerializer(
                                data=order_product_data)
                            if order_product_serializer.is_valid():
                                order_product_serializer.save()
                            else:
                                raise serializers.ValidationError(
                                    order_product_serializer.errors)

                        return Response({"message": "Order placed successfully"}, status=status.HTTP_201_CREATED)

        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Cart product created or updated successfully"}, status=status.HTTP_201_CREATED)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
