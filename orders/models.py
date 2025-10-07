from django.db import models

from .models import OrderStatus # if OrderStatus is in the same app(orders)
#or: from orders.models import OrderStatus
from django.contrib.auth.models import User
from menu.models import MenuItem
from .models import OrderStatus
from decimal import Decimal 
from django.utils import timeZone
from decimal import Decimal, ROUND_HALF_UP
import logging
from django.conf import settings


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
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    Created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Preocessing', 'Processing'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order {self.id} - {self.status}"

        def calculate_total(self):
            total = Decimal("0.00")
            for item in self.items.all():
                total += item.price * item.quantity
            return total

class OrderItem(models.Model):
    order = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    menu_item = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} (order {self.order.id})"

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_until = models.DateField()

    def __str__(self):
        return f"{self.code} ({self.discount_percentage}% off)"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

logger = logging.getLogger(__name__)

try:
    from .utils import calculate_discount
except Exception:
    calculate_discount = None
    logger.debug("calculate_discount utility not available; discounts will be skipped.")

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self, apply_discount: bool = True, coupon_code: str = None, save: bool = False) -> Decimal:
        total = Decimal('0.00')

        for item in getattr(self, 'items').all():
            price = item.price if item.price is not None else Decimal('0.00')
            qty = getattr(item, 'quantity', 1) or 0

            line_total = (Decimal(price) * Decimal(qty))
            total += line_total

        total = total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        if apply_discount and coupon_code and calculate_discount:
            try:
                discount_value = calculate_discount(total, coupon_code)
                if discount_value is None:
                    pass
                else:
                    discount_dec = Decimal(str(discount_value))

                    if Decimal('0') < discount_dec <= Decimal('1'):
                        discount_amount = (total * discount_dec).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

                        else:
                            discount_amount = discount_dec.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

                        total_after = total - discount_amount
                        if total_after < Decimal('0.00'):
                            total_after = Decimal('0.00')
                        total = total_after.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                except Exception as exc:
                    logger.exception("Error applying discount for order %s with coupon '%s':%s", self.pk, coupon_code, exc)
            
            if save:
                try:
                    self.total_price = total
                    self.save(update_fields=['total_price'])
                except Exception:
                    logger.exception("Failed to save calculated total for order %s", getattr(self, 'pk', None))

            return total