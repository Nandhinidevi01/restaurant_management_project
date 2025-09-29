from rest_framework import serializers
from home.models import MenuCategory
from home.models import MenuItem  #assuming you have a MenuItem model
from .models import ContactFormSubmission


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

class ContactFormSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactFormSubmission
        fields = ['id', 'name', 'email', 'message', 'submitted_at']