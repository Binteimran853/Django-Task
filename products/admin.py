from django.contrib import admin

from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("image", "name", "price", "category")
    list_filter = (
        "category",
        "price",
    )
    search_fields = (
        "name",
        "category__name",
    )
    list_editable = (
        "price",
        "category",
        "name",
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
