from django.test import TestCase
from django.contrib.auth.models import User
from home.models import MenuItem
from .models import Order, OrderItem

class OrderModelTest(TestCase):
    def setup(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.order = Order.objects.create(user=self.user)

        menu_item1 = MenuItem.objects.create(
            restaurant_id=1, name="paneer Butter Masala", price=200, is_available=True
        )
        menu_item2 = MenuItem.objects.create(
            restaurant_id=1, name="Naan", price=50, is_available=True
        )

        OrderItem.objects.create(order=self.order, menu_item=menu_item1, quantity=2, price=200)
        OrderItem.objects.create(order=self.order, menu_item=menu_item2, quantity=3, price=50)

        def test_calculate_total(self):
            total = self.order.calculate_total()
            self.assertEqual(total, 2*200 + 3*50)

        def save(self, *args, **kwargs):
            self.total_price = self.calculate_total()
            super().save(*args, **kwargs)