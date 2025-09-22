from django.urls import path
from .views import MenuItemsByCategoryView

urlpatterns = [
    path('menu-items-by-category/', MenuItemsByCategoryView.as_view(), name='menu-items-by-category'),
]