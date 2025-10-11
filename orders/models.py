from django.db import models

# Create your models here.
from .models import OrderStatus # if OrderStatus is in the same app(orders)
#or: from orders.models import OrderStatus
from django.contrib.auth.models import User
from menu.models import MenuItem
from .models import OrderStatus
from .utils import generate_unique_order_id


class order(models.Model):
    # existing fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    customer = models.CharField(max_length=200)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    Created_at = models.DateTimeField(auto_now_add=True)

    #Now field for order status
    status = models.ForeignKey(
        OrderStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"

class OrderStatus(models.Model):
    """
    Represents different statuses for an order
    """
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

from orders.utils import generate_coupon_code

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)  #Example

    def save(self, *args, **kwargs):
        if not self.code: #Auto-generate only if empty
            self.code = generate_coupon_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.discount}%"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    Created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} (x{self.quantity})"
        
class ActiveOrderManager(models.Manager):
    def get_active_orders(self):
        # Return only orders with status 'pending' or 'processing'
        return super().get_queryset().filter(status__in=['pending', 'processing'])

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    #custom manager
    objects = ActiveOrderManager()

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username} - {self.status}"

from Orders.models import Order

#create some test orders
Order.objects.create(customer_id=1, total_price=200, status="pending")
Order.objects.create(customer_id=1, total_price=150, status="processing")
Order.objects.create(customer_id=1, total_price=300, status="completed")

# Retrieve only active orders
active_orders = Order.objects.get_active_orders()
print(active_orders)


class Order(models.Model):
    order_id = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
        default=generate_unique_order_id
    )
    #other fields for your order
    customer_name = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    Created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

class OrderManager(models.Model):
    def with_status(self, status):
        """ Retrieve all orders with a specific status (e.g., 'pending', 'completed')."""
        return self.with_status('pending')

    def completed(self):
        """Shortcut for retrieving all completed orders."""
        return self.with_status('completed')

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    Created_at = models.DateTimeField(auto_now_add=True)

    objects = OrderManager()

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} ({self.status})"