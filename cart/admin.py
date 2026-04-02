from django.contrib import admin

from cart.models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user")


class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "cart",
        "product_name",
        "product_price",
        "product_category",
        "quantity",
    )
    list_filter = ("cart__user__username", "product__category")
    search_fields = (
        "cart",
        "product__category",
    )

    @admin.display(description="Price")
    def product_price(self, obj):
        return obj.product.price

    @admin.display(description="Category")
    def product_category(self, obj):
        return obj.product.category

    @admin.display(description="Name")
    def product_name(self, obj):
        return obj.product.name


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
