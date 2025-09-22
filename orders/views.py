from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response 
from rest_framework import status, views
from utils.validation_utils import validate_email_address

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