
from rest_framework import viewsets
# Create your views here.
from . import models
from . import serializers


class OrderViewset(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
