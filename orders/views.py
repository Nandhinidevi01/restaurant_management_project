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
from rest_framework.generics import RetrieveAPIView
from .serializers import OrderDetailSerializer
from orders.utils import send_order_confirmation_email
from .utils import generate_unique_order_id


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
        
class OrderDetailView(RetrieveAPIView):
    """
    Retrieve details of a specific order by ID.
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

def place_order(request):
    #Example usage after creating an order
    order = ... #your order instance
    response = send_order_confirmation_email(
        order_id=order.id,
        customer_email=order.user.email,
        user_name=order.user.username,
        total_price=order.total_price, 
    )
    print(response)  #for debugging


def create_order(request):
    if request.method == 'POST':
        order = Order.objects.create(
            order_id=generate_unique_order_id(),
            customer_name=request.POST.get('customer_name'),
            total_amount=request.POST.get('total_amount')
        )
        return render(request, 'orde_succes.html', {'order': oreder})