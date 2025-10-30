from django.urls import path
from .views import OrderHistoryView
from .views import OrderDetailView
from .views import CancelOrderView
from .views import CouponValidationView
from .views import UpdateOrderStatusView
from .views import UpdateOrderStatusAPIView
from . import views
from .views import OrderStatusView 


urlpatterns = [
    path('order-history/', OrderHistoryView.as_view(), name='order-history'),
]

urlpatterns1 = [
    path('<int:id>/', OrderDetailView.as_view(), name='order-detail'),
]

urlpatterns2 = [
    path('orders/<int:order_id>/cancel/', CancelOrderView.as_view(), name='Cancel-order'),
]

urlpatterns3 = [
    path('coupons/validate/', CouponValidationView.as_view(), name='coupon_validate')
]

urlpatterns4 = [
    path('orders/<int:order_id>/update_status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
]

urlpatterns5 = [
    path('orders/update-status/', UpdateOrderStatusAPIView.as_view(), name='update-order-status'),
]

urlpatterns6 = [
    path('status/<int:order_id>/', views.get_order_status, name='get_order_status'),
]

urlpatterns7 = [
    path('status/<str:short_id>/', OrderStatusView.as_view(), name='order-status'),
]