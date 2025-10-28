from django.urls import path
from home.views import MenuCategoryListView
from home.views import MenuItemSearchViewSet
from home.views import MenuItemUpdateViewSet
from .views import TableDetailView
from .views import AvailableTablesAPIView
from django.urls import include
from .views import ReviewCreateAPIView
from .views import MenuItemIngredientsView
from .views import FeaturedMenuItemsView
from home.views import MenuItemSearchAPIView


urlpatterns = [
    path('categories/', MenuCategoryListView.as_view(), name='menu-categories'),
]

menu_item_search = MenuItemSearchViewSet.as_view({'get': 'list'})
urlpatterns1 = [
    path('menu-items/search/', menu_item_search, name='menu-item-search'),
]

menu_item_update = MenuItemUpdateViewSet.as_view({'put': 'update'})
urlpatterns2 = [
    path('menu-item/<int:pk>/update/', menu_item_update, name='menu-item-update'),
]

urlpatterns3 = [
    path("api/tables/<int:pk>/", TableDetailView.as_view(),name="table-detail"),
]

urlpatterns4 = [
    path('api/tables/available/', AvailableTablesAPIView.as_view(), name='available_tables_api'),
]

urlpatterns5 = [
    path('api/', include('menu.urls')),
]

urlpatterns6 = [
    path('reviews/create/', ReviewCreateAPIView.as_view(), name='create-review'),
]

urlpatterns7 = [
    path('api/menu-items/<int:pk>/ingredients/', MenuItemIngredientsView.as_view(), name='menu-item-ingredients'),
]

urlpatterns8 = [
    path('featured-menu-items/', FeaturedMenuItemsView.as_view(), name='featured-menu-items'),
]

urlpatterns9 = [
    path('menu/search/', MenuItemSearchAPIView.as_view(), name='menu-item-search'),
]