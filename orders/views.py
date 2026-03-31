import stripe
from django.conf import settings
from django.shortcuts import redirect, render,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from carts.models import Cart
from .models import Order, OrderItem


# ✅ Stripe Setup
stripe.api_key = settings.STRIPE_SECRET_KEY


# =========================
# CREATE ORDER FROM CART
# =========================
def create_order_from_cart(user):
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return None

    items = cart.items.select_related('product')

    if not items.exists():
        return None

    order = Order.objects.create(
        user=user,
        total_amount=0,
        status='PENDING'
    )

    total = 0

    for item in items:
        price_inr = float(item.product.price)  # 2000.0 INR

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=price_inr
        )

        total += price_inr * item.quantity

    order.total_amount = total
    order.save()

    return order


# =========================
# CHECKOUT (STRIPE)
# =========================
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    order = create_order_from_cart(request.user)

    if not order:
        return redirect('carts:cart')

    line_items = []

    for item in order.items.all():
        line_items.append({
            "price_data": {
                "currency": "inr",
                "product_data": {
                    "name": item.product.name,
                },
                "unit_amount": item.price,
            },
            "quantity": item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',

        success_url='http://127.0.0.1:8000/orders/success/?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/orders/cancel/',

        metadata={
            "order_id": order.id
        }
    )


    order.stripe_session_id = session.id
    order.save()
 
    return redirect(session.url)


# =========================
# SUCCESS PAGE (UI ONLY)
# =========================
def payment_success(request):
    session_id = request.GET.get('session_id')

    if not session_id:
        return render(request, 'orders/payment_failed.html')

    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == 'paid':
        order_id = session.metadata['order_id']  # ✅ FIXED

        order = Order.objects.get(id=order_id)
        order.status = 'PAID'
        order.save()

    print("Order marked as PAID:", order.id)

    return render(request, 'orders/payment_success.html')

# =========================
# CANCEL PAGE
# =========================
def payment_cancel(request):
    return render(request, 'orders/payment_failed.html')


# =========================
# STRIPE WEBHOOK
# =========================
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # ✅ PAYMENT SUCCESS
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        session_id = session.get('id')
        payment_intent = session.get('payment_intent')

        try:
            order = Order.objects.get(stripe_session_id=session_id)

            order.status = 'PAID'
            order.stripe_payment_intent = payment_intent
            order.save()

            # ✅ Clear Cart
            Cart.objects.filter(user=order.user).delete()

            print("Webhook triggered")
            print("Event:", event['type'])

        except Order.DoesNotExist:
            pass

    # ❌ PAYMENT FAILED / EXPIRED
    elif event['type'] in ['checkout.session.expired']:
        session = event['data']['object']
        session_id = session.get('id')

        Order.objects.filter(
            stripe_session_id=session_id
        ).update(status='FAILED')

    return HttpResponse(status=200)


def order_history(request):
    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'orders/history.html', {
        'orders': orders
    })


def order_detail(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user   # 🔐 SECURITY
    )

    items = order.items.select_related('product')

    return render(request, 'orders/detail.html', {
        'order': order,
        'items': items
    })