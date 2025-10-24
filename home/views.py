from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from home.models import MenuCategory
from home.serializers import MenuCategorySerializer
from rest_framework import viewSets, filters
from rest_framework.response import Response 
from home.models import MenuItem
from home.serializers import MenuItemSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from .utils import send_email
from rest_framework import generics, permissions
from .models import Table
from .serializers import TableSerializer
from .serializers import DailySpecialSerializer
from .models import UserReview
from .serializers import UserReviewSerializer
from rest_framework.views import APIView
from rest_framework import permissions
from .models import MenuCategory
from .serializers import MenuCategorySerializer 



class MenuCategoryListView(ListAPIView):
    """
    API endpoint to list all menu categories.
    """

    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

class MenuItemPagination(PageNumberPagination):
    page_size = 10 #default items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class MenuItemSearchViewSet(viewSets.viewSet):
    """
    API endpoint to search for menu items by name.
    """
    pagination_class = MenuItemPagination

    def list(self, request):
        query = request.query_params.get('q','') #?q=pizza
        items = MenuItem.objects.filter(name_icontains = query)

        #Apply pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(items, request)
        serializer = MenuItemSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

class MenuItemUpdateViewSet(viewsets.viewSet):
    """
    API endpoint to update an existing menu item.
    Only admin users can update.
    """
    permission_classes = [IsAdminUser]

    def update(self, request, pk=None):
        try:
            menu_item = MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return Response(
                {"error": "Menu item not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = MenuItemSerializer(menu_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

@api_view(['POST'])
def contact_restaurant(request):
    name = request.data.get("name")
    email = request.data.get("email")
    message = request.data.get("message")

    subject = f"New COntact Form Submission from {name}"
    body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"

    if send_email("restaurant@example.com", subject, body):
        return Response({"message": "Your message was sent successfully."}, status=200)
    else:
        return Response({"error": "Failed to send email."}, status=500)

class TableDetailView(generics.RetrieveAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    lookup_field = "pk" # Default, can be omitted

class AvailableTablesAPIView(generics.ListAPIView):
    serializer_class = TableSerializer

    def get_queryset(self):
        return Table.objects.filter(is_available=True)

class DailySpecialListView(generics.ListAPIView):
    queryset = MenuItem.objects.filter(is_daily_special=True)
    serializer_class = DailySpecialSerializer

class UserReviewCreateView(generics.CreateAPIView):
    queryset = UserReview.objects.all()
    serializer_class = UserReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MenuItemReviewsView(APIView):
    """
    Retrieve all reviews for a given menu_item_id
    """
    def get(self, request, menu_item_id):
        reviews = UserReview.objects.filter(menu_item_id=menu_item_id)
        if not reviews.exists():
            return Response({"message": "No reviews found for this item."}, status=status.HTTP_404_BAD_REQUEST)

        serializer = UserReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MenuCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows menu categories to be viewed or edited.
    Supports: list, retrieve, create, update, and delete.
    """
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    from .utils import calculate_order_total

    def sample_order_view(request):
        order_item = [
            {"price": 100.0, "quantity": 2},
            {"price": 50.0, "quantity": 3},
        ]
        total = calculate_order_total(order_item)
        print("order Total:", total)
        return JsonResponse({"total": total})

class MenuCategoryViewSet(viewSets.ModelViewSet):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

class MenuCategoryListView(generics.ListAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer