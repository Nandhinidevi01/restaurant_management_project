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
from django.shortcuts import get_object_or_404


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

class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        if order.user != request.user:
            return Response({"error": "You are not authorized to cancel this order."},status=status.HTTP_403_FORBIDDEN)

        if order.status in ["Cancelled", "Completed"]:
            return Response({"error": f"Order already {order.status}."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = "Cancelled"
        Order.save()

        return Response({"message": "Order Cancelled successfully.",
                        "order": OrderSerializer(order).data},
                        status=status.HTTP_200_OK)