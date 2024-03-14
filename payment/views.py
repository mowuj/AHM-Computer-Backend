from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer
from customer.models import Customer
import stripe
from decimal import Decimal 
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
DOMAIN = 'https://ahm-computer-backend.onrender.com'


class PaymentViewset(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def create(self, request, *args, **kwargs):
        customer_id = request.data.get('customer')
        amount = request.data.get('amount')

        serializer = self.get_serializer(
            data={'customer': customer_id, 'amount': amount})
        serializer.is_valid(raise_exception=True)

        customer = Customer.objects.get(id=customer_id)

        amount_decimal = Decimal(amount)

        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount_decimal * 100),
            currency='inr',
            customer=customer,
        )

        payment = Payment.objects.create(
            customer=customer,
            amount=amount_decimal,
        )

        return Response({'client_secret': payment_intent.client_secret}, status=status.HTTP_201_CREATED)
