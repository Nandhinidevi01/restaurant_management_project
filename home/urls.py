from django.urls import path
from home.views import MenuCategoryListView

urlpatterns = [
    path('categories/', MenuCategoryListView.as_view(), name='menu-categories'),
]