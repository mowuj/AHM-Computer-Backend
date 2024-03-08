
from rest_framework import viewsets
# Create your views here.
from . import models
from . import serializers


class OrderViewset(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

class OrderProductViewset(viewsets.ModelViewSet):
    queryset = models.OrderProduct.objects.all()
    serializer_class = serializers.OrderProductSerializer

class ShipmentViewset(viewsets.ModelViewSet):
    queryset = models.Shipment.objects.all()
    serializer_class = serializers.ShipmentSerializer
