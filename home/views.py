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