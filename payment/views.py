from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from .models import Details
from . import serializers


class BillingDetailsViewset(viewsets.ModelViewSet):
    serializer_class = serializers.BillingDetailsSerializer
    queryset = Details.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            serializer.object.get[user] = user
            serializer.save()
            return Response('Your Billing Details have been Saved')
        return Response(serializer.errors())


class ShowUserBillingDetails(APIView):
    def get(self, request):
        user = request.user
        data = Details.objects.filter(user=user)
        if data.exists():
            serializer = serializers.BillingDetailsSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No billing details found for this user."}, status=status.HTTP_404_NOT_FOUND)


class UpdateBillingDetails(APIView):
    def put(self, request, id):
        user = request.user
        try:
            billing_details = Details.objects.get(
                pk=id, user=user)
        except Details.DoesNotExist:
            return Response({"detail": "Billing details not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.BillingDetailsSerializer(
            billing_details, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
