from django.urls import path
from .views import OrderHistoryView
from .views import OrderDetailView
from .views import CancelOrderView


urlpatterns = [
    path('order-history/', OrderHistoryView.as_view(), name='order-history'),
]

urlpatterns1 = [
    path('<int:id>/', OrderDetailView.as_view(), name='order-detail'),
]

urlpatterns2 = [
    path('orders/<int:order_id>/cancel/', CancelOrderView.as_view(), name='Cancel-order'),
]