from django.db import models

# Create your models here.
from .models import OrderStatus # if OrderStatus is in the same app(orders)
#or: from orders.models import OrderStatus

class order(models.Model):
    # existing fields
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