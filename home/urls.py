from django.urls import path
from home.views import MenuCategoryListView
from home.views import MenuItemSearchViewSet
from home.views import MenuItemUpdateViewSet
from .views import TableDetailView
from .views import AvailableTablesAPIView
from .views import DailySpecialListView
from .views import UserReviewCreateView, MenuItemReviewsView
from django.urls import include
from rest_framework.routers import DefaultRouter
from .views import MenuCategoryViewSet


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
    path('daily-specials/', DailySpecialListView.as_view(), name='daily-specials'),
]

urlpatterns6 = [
    path('reviews/create/', UserReviewCreateView.as_view(), name='create_review'),
    path('reviews/<int:menu_item_id>/', MenuItemReviewsView.as_view(), name='menu_item_reviews'),
]

router = DefaultRouter()
router.register(r'categories', MenuCategoryViewSet, basename='menu-category')

urlpatterns7 = [
    path('', include(router.urls)),
]

router = DefaultRouter()
router.register(r'menu-categories', MenuCategoryViewSet, basename='menu-category')

urlpatterns8 = [
    path('', include(router.urls)),
]