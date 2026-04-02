from django.contrib import admin

from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "payment_status", "created_at")
    list_filter = ("payment_status", "created_at", "user")
    search_fields = ("id", "user__username", "user__email", "payment_status")


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")
    list_filter = ("product", "order__user")
    search_fields = (
        "product__name",
        "order__id",
        "order__user__username",
        "order__user__email",
    )


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
