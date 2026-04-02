from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def home(request):
    category = Category.objects.all()
    products = Product.objects.all()
    return render(request, "home.html", {"categories": category, "products": products})


def products_list(request, fk):

    products = Product.objects.filter(category=fk)
    return render(request, "products.html", {"products": products})


def product_detail(request, pk):

    pk = int(pk)
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})
