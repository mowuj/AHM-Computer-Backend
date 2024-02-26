from rest_framework import serializers
from .models import Details


class BillingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = '__all__'
