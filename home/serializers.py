from rest_framework import serializers
from home.models import MenuCategory
from home.models import MenuItem  #assuming you have a MenuItem model

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
        fields = ['id', 'name', 'price', 'description', 'category'] # adjust fields as per your model
        