import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from cart.models import Cart, CartItem
from Order.models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required(login_url="login")
def check_out(request, cart_id):
    """
    Creates an order from the user's cart and redirects to Stripe checkout.
    """
    domain = request.build_absolute_uri("/")  # dynamic base URL
    cart = Cart.objects.get(pk=cart_id)
    cart_item = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_item)
    order = Order.objects.create(user=request.user, total_amount=total_price)

    for item in cart_item:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

    line_items = []
    for item in cart_item:
        if item.quantity <= 0:
            continue
        line_items.append(
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(item.product.price * 100),
                    "product_data": {
                        "name": item.product.name,
                    },
                },
                "quantity": item.quantity,
            }
        )

    checkout_session = stripe.checkout.Session.create(
        line_items=line_items,
        mode="payment",
        customer_email=request.user.email,
        success_url=f"{domain}success/",
        cancel_url=f"{domain}cancel/",
        metadata={
            "order_id": str(order.id),
        },
        payment_intent_data={
            "metadata": {
                "order_id": str(order.id),
                "cart_id": str(cart.id),
            }
        },
    )

    return redirect(checkout_session.url, code=303)


@csrf_exempt
def stripe_webhook(request):
    """
    Handles Stripe webhook events.
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        print("[ERROR] Invalid payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        print("[ERROR] Invalid Stripe signature")
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session.get("metadata", {})
        order_id = metadata.get("order_id")
        cart_id = metadata.get("cart_id")

        try:
            order = Order.objects.get(id=order_id)
            order.payment_status = "Paid"
            order.save()
            try:
                cart = Cart.objects.get(user=order.user)
                CartItem.objects.filter(cart=cart).delete()
                cart.delete()
                print(f"Cart for user {order.user.username} cleared successfully")
            except Cart.DoesNotExist:
                print(f"No cart found for user {order.user.username}")
            print("Order updated successfully")
        except Order.DoesNotExist:
            print("Order not found for ID:", order_id)

    elif event["type"] == "payment_intent.payment_failed":
        intent = event["data"]["object"]
        order_id = intent.get("metadata", {}).get("order_id")

        try:
            order = Order.objects.get(id=order_id)
            order.payment_status = "Pending"
            order.save()
            print(f"Order {order_id} payment FAILED")
        except Order.DoesNotExist:
            print("Order not found for ID:", order_id)

    else:
        print(f"[INFO] Unhandled Stripe event type: {event.get('type')}")

    return HttpResponse(status=200)


def success(request):
    return render(request, "success.html")


def cancel(request):
    return render(request, "cancel.html")
