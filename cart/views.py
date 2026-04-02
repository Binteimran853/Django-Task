from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product

from .models import Cart, CartItem


@login_required(login_url="login")
def user_cart(request):

    cart, create_cart = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart, quantity__gt=0)
    total_price = sum(item.quantity * item.product.price for item in items)

    return render(
        request, "cart.html", {"cart": cart, "items": items, "total_price": total_price}
    )


@login_required(login_url="login")
def add_cart(request, pk):

    product = get_object_or_404(Product, pk=pk)
    cart, create_cart = Cart.objects.get_or_create(user=request.user)
    cart_item, create_cart_item = CartItem.objects.get_or_create(
        cart=cart, product=product
    )

    if not create_cart_item:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()
    messages.success(request, "Items added successfully !!")

    if request.method == "POST":
        return redirect(request.META.get("HTTP_REFERER"), "home")
    return redirect("cart")


@login_required(login_url="login")
def update_cart(request, item_id, action):

    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, pk=item_id)
        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease":
            cart_item.quantity -= 1

        CartItem.objects.filter(quantity__lte=0).delete()
        cart_item.save()

    return redirect(request.META.get("HTTP_REFERER", "/cart/"))
