from django.db import path
from .views import UpdateMenuItemAvailabilityView

urlpatterns = [
    path('menu/<int:pk>/availability/', UpdateMenuItemAvailabilityView.as_view(), name='update-menu-availability'),
]