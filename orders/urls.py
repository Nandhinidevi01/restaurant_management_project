from django.urls import path
from .views import OrderHistoryView
from .views import OrderDetailView

urlpatterns = [
    path('order-history/', OrderHistoryView.as_view(), name='order-history'),
]

urlpatterns1 = [
    path('<int:id>/', OrderDetailView.as_view(), name='order-detail'),
]