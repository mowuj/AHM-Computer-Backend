from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Customer


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    image = serializers.ImageField(required=False, write_only=True)
    mobile_no = serializers.CharField(required=True, write_only=True)
    address = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password',
                  'confirm_password', 'image', 'mobile_no', 'address']

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']

        image = self.validated_data.get('image', None)
        mobile_no = self.validated_data['mobile_no']
        address = self.validated_data.get('address', None)

        if password != password2:
            raise serializers.ValidationError(
                {'error': "Password Doesn't Matched"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'error': "Email Already exists"})

        # Create User
        user = User(username=username, email=email,
                    first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.is_active = False
        user.save()

        # Explicitly set user_id when creating Customer
        customer_data = {
            'user_id': user.id,
            'image': image,
            'mobile_no': mobile_no,
            'address': address,
        }
        customer = Customer.objects.create(**customer_data)

        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = User.objects.filter(username=username).first()

            if user and user.check_password(password):
                return data
            raise serializers.ValidationError(
                "Incorrect username or password.")
        else:
            raise serializers.ValidationError(
                "Both username and password are required.")


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
