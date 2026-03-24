from django.shortcuts import render, get_object_or_404

from .models import Product, Category


def home(request):
    category = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'home.html', {
        'categories': category, 'products': products
    })


def products_list(request, fk):
    print(request.method)
    print(request.user)
    products = Product.objects.filter(category=fk)
    return render(
        request, 'products.html', {'products': products}
    )


def product_detail(request, pk):
    print(request.method)
    print(request.user)
    pk = int(pk)
    product = get_object_or_404(Product, pk=pk)
    print(product)
    return render(
        request, 'product_detail.html', {'product': product}
    )
