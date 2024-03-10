from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from .models import Payment
from . import serializers


class PaymentViewset(viewsets.ModelViewSet):
    serializer_class = serializers.PaymentSerializer
    queryset = Payment.objects.all()
