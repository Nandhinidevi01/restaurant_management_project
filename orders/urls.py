from django.urls import path
from .views import OrderHistoryView

urlpatterns = [
    path('order-history/', OrderHistoryView.as_view(), name='order-history'),
]