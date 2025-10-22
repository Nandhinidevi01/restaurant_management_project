from django.db import models
from django.contrib.auth.models import User

class MenuCategory(models.Model):
    """
    Represents a category for the resturant's menu
    """
    name = models.CharField(max_length = 100, unique = True)

    def __str__(self):
        return self.name

class Review(models.Model):
    """
    Model to represent a user review with rating and text feedback.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating} Stars"