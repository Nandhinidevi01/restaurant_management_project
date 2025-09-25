from django.urls import path
from .views import *
from .views import UserProfileViewSet


urlpatterns = [
    path('items/', ItemView.as_view(), name='item-list'),
]

urlpatterns1 = [
    path('profile/update/', user_profile_update, name="user-profile-update",)
]