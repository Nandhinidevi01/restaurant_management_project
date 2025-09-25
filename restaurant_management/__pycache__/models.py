from django.db import models
from restaurant.models import Restaurant


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    # New field for operating days
    opening_days = models.CharField(
        max_length=100,
        help_text="Comma-separated days (e.g., Mon,Tue,Wed,Thu,Fri,Sat,Sun",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

r = Restaurant.objects.create(
    name="Food Paradise",
    address="123 Main Street",
    phone="98765432140"
    opening_days="Mon,Tue,Wed,Thu,Fri,Sat"
)
print(r.opening_days)