from django.urls import path, include
from .views import MenuItemsByCategoryView
from django.contrib import admin

urlpatterns = [
    path('menu-items-by-category/', MenuItemsByCategoryView.as_view(), name='menu-items-by-category'),
]

urlpatterns1 = [
    path('admin/', admin.site.urls),
    path('api/home/', include('home.urls')),
]