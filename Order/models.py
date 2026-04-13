from django.conf import settings
from django.db import models

from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Paid", "Paid")],
        default="Pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    receipt_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot

    def __str__(self):
        return f"{self.product} - {self.quantity}"
