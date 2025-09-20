from django.db import models

class MenuCategory(models.Model):
    """
    Represents a category for the resturant's menu
    """
    name = models.CharField(max_length = 100, unique = True)

    def __str__(self):
        return self.name