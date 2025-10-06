from rest_framework import serializers
from .models import Order, OrderItem
from .models import Coupon


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

class CouponSerislizer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_percentage', 'is_active', 'valid_from', 'valid_until']

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status']

    def validate_status(self, value):
        allowed_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if value not in allowed_statuses:
            raise serializers.ValidationError(f"Invalid status. Must be one of: {', '.join(allowed_statuses)}.")
        return value