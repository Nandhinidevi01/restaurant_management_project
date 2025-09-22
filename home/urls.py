from django.urls import path
from home.views import MenuCategoryListView
from home.views import MenuItemSearchViewSet

urlpatterns = [
    path('categories/', MenuCategoryListView.as_view(), name='menu-categories'),
]

menu_item_search = MenuItemSearchViewSet.as_view({'get': 'list'})
urlpatterns1 = [
    path('menu-items/search/', menu_item_search, name='menu-item-search'),
]