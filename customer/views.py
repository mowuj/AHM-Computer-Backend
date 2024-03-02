from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from django.db import IntegrityError, transaction
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from customer.models import Customer
from .serializers import RegistrationSerializer, CustomerProfileSerializer, CustomerSerializer


class UserRegistrationApiView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()

                    # Explicitly check if a Customer object exists
                    customer, created = Customer.objects.get_or_create(
                        user=user,
                        defaults={
                            'image': serializer.validated_data.get('image'),
                            'mobile_no': serializer.validated_data.get('mobile_no'),
                            'address': serializer.validated_data.get('address'),
                        }
                    )

                    if not created:
                        # If customer already exists, update the fields
                        customer.image = serializer.validated_data.get('image')
                        customer.mobile_no = serializer.validated_data.get(
                            'mobile_no')
                        customer.address = serializer.validated_data.get(
                            'address')
                        customer.save()

                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    confirm_link = f"https://ahm-computer-backend.onrender.com/customer/active/{uid}/{token}"
                    email_subject = "Confirm Your Email"
                    email_body = render_to_string(
                        'email.html', {'confirm_link': confirm_link})
                    email = EmailMultiAlternatives(
                        email_subject, '', to=[user.email])
                    email.attach_alternative(email_body, "text/html")
                    email.send()

                    login(request, user)

                    return Response("Check your email for confirmation and login.", status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                # Log the error for further investigation
                print(f"ERROR: {str(e)}")
                return Response(f"An error occurred during registration: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login') 
    else:
        return redirect('register') 

class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)

                login(request, user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': "Invalid Credential"})
        return Response(serializer.errors)


class UserLogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')



class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = models.Customer.objects.filter(user=user)
        return queryset


class CustomerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerProfileSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = models.UserProfile.objects.filter(user=user)
        return queryset
