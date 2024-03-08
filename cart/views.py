from django.shortcuts import render
from .models import Cart,CartProduct
from .serializers import CartSerializer,CartProductSerializer
from order.serializers import OrderSerializer,OrderProductSerializer
# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from rest_framework.decorators import action
class CartViewset(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartProductViewset(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

    @action(detail=False, methods=['post'])
    def create_order(self, request, *args, **kwargs):
        cart_id = request.data.get('cart')
        ordered_by = request.data.get('ordered_by')
        order_status = request.data.get('order_status', 'Order Received')

        try:
            with transaction.atomic():
                cart_products = CartProduct.objects.filter(cart=cart_id)
                total_amount = sum(
                    cart_product.subtotal for cart_product in cart_products)

                order_data = {
                    "cart": cart_id,
                    "ordered_by": ordered_by,
                    "total_amount": total_amount,
                    "order_status": order_status,
                }

                order_serializer = OrderSerializer(data=order_data)
                order_serializer.is_valid(raise_exception=True)
                order_instance = order_serializer.save()

                for cart_product in cart_products:
                    order_product_data = {
                        "order": order_instance.id,
                        "product": cart_product.product.id,
                        "price": cart_product.price,
                        "quantity": cart_product.quantity,
                        "subtotal": cart_product.subtotal,
                    }
                    order_product_serializer = OrderProductSerializer(
                        data=order_product_data)
                    order_product_serializer.is_valid(raise_exception=True)
                    order_product_serializer.save()

                return Response({"message": "Order placed successfully"}, status=status.HTTP_201_CREATED)

        except IntegrityError as integrity_error:
            return Response({"error": str(integrity_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ValidationError as validation_error:
            return Response({"error": str(validation_error)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
