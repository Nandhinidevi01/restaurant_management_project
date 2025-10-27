from django.contrib import admin
from .models import Restaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'email')

    search_fields = ('name', 'address')

    list_filter = ('is_active',)