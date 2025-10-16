from django.urls import path
from .views import RestaurantInfoView
from django.urls import include

urlpatterns = [
    path('info/', RestaurantInfoView.as_view(), name='restaurant info'),
]

urlpatterns1 = [
    path('api/restaurant/', include('restaurant.urls')),
]