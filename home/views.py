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
from rest_framework import generics
from .models import Table
from .serializers import TableSerializer
from rest_framework.views import APIView 
from .serializers import ReviewSerializer
from home.models import DailySpecial
from django.shortcuts import render


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

class ReviewCreateAPIView(APIView):
    """
    API endpoint tp handle the creation of user reviews via POST request.
    """

    def post(self, request, *args, **kwargs):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Review created successfully!", "data": serializer.data},
                status=status.HTTP_200_CREATED
            )
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_404_BAD_REQUEST
        )

def homepage(request):
    special = DailySpecial.get_random_special()
    return render(request, 'home/index.html', {'special': special})