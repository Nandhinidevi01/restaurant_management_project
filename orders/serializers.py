from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source="menu_item.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ['menu_item_name', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'total_price', 'status', 'items', 'user']
        
class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_name = serializers.CharField(source="status.name", read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ["id", "user", "created_at", "total_price", "status_name", "items"]
        