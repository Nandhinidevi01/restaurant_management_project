from rest_framework import serializers
from home.models import MenuCategory

class MenuCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for MenuCategory model.
    """

    class Meta:
        model = MenuCategory
        fields = ['id', 'name'] #include id for frontend reference
        