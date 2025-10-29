from django.db import models
from django.contrib.auth.models import User
import random
from django.db.models import Count


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


class DailySPecial(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_length=6, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_random_special():
        """
        Fetch a random DailySpecial from the database.
        Returns:
            DailySpecial instance if available, else None.
        """
        specials = DailySPecial.objects.filter(is_available=True)
        if not specials.exists():
            return None
        return specials.order_by('?').first()

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_length=6, decimal_places=2)
    ingredients = models.ManyToManyField(Ingredient, related_name='menu_items', blank=True)

    def __str__(self):
        return self.name

class MenuItemManager(models.Manager):
    def get_top_selling_items(self, num_items=5):
        return self.annotate(
            total_orders=Count('orderitem')
        ).order_by('-total_orders')[:num_items]

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    objects = MenuItemManager()

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='orderitem')
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Cuisine(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, related_name='menu_items')

    def __str__(self):
        return self.name
        
class OpeningHour(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday'), ('Friday'),
        ('Saturday'), ('Saturday'),
        ('Sunday'), ('Sunday'),
    ]

    day = models.CharField(max_length=10, choices=DAY_CHOICES, unique=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.day}: {self.opening_time} - {self.closing_time}"