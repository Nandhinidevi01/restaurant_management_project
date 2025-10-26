from rest_framework import serializers
from home.models import MenuCategory
from home.models import MenuItem  #assuming you have a MenuItem model
from .models import Table
from .models import Review
from .models import Ingredient


class MenuCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for MenuCategory model.
    """

    class Meta:
        model = MenuCategory
        fields = ['id', 'name'] #include id for frontend reference
        
class MenuItemSerializer(serializers.ModelSerializer):
    """
    Serializer for MenuItem model.
    """
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'description', 'category', 'availability'] # adjust fields as per your model
        
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'table_number', 'capacity', 'is_available']

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model to validate and serializer review data.
    """
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class MenuItemIngredientsSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'ingredients']