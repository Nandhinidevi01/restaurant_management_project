from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response 
from rest_framework import status, views
from utils.validation_utils import validate_email_address
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer


class SignupView(views.APIView):
    def post(self, request):
        email = request.data.get("email")

        if not validate_email_address(email):
            return Response(
                {"error": "Invalid email address"},
                status=status.HTTP_400_BAD_REQUEST
            )

        #proceed with user creation
        return Response(
            {"message": "Email validated_successfully"},
            status=status.HTTP_200_OK
        )


class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve order history for the logged in user.
        """

        user = request.user
        orders = Order.objects.filter(user=user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        