from django.shortcuts import render,redirect
import razorpay
from django.conf import settings
from django.http import HttpResponse
# Create your views here.

from carts.models import Cart, CartItem
from orders.models import Order, OrderItem  # adjust if same app


def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    cart = Cart.objects.filter(user=request.user).first()
    items = CartItem.objects.filter(cart=cart)

    total = sum(item.product.price * item.quantity for item in items)

    # 💰 Razorpay works in paise
    amount = int(total * 100)

    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    payment = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'payment_capture': 1
    })

     # Save order
    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        razorpay_order_id=payment['id']
    )

    return render(request, 'order/checkout.html', {
        'payment': payment,
        'order': order,
        'razorpay_key': settings.RAZORPAY_KEY_ID
    })

def payment_success(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    signature = request.GET.get('signature')

    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })

        order = Order.objects.get(razorpay_order_id=order_id)
        order.razorpay_payment_id = payment_id
        order.razorpay_signature = signature
        order.is_paid = True
        order.save()

        return HttpResponse("✅ Payment Successful")

    except:
        return HttpResponse("❌ Payment Failed")



def payment_failed(request):
    return HttpResponse("❌ Payment Cancelled or Failed")





def place_order(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = Cart.objects.filter(user=request.user).first()
    items = CartItem.objects.filter(cart=cart)

    if not items:
        return HttpResponse("Cart is empty")

    # 💰 Calculate total
    total = sum(item.product.price * item.quantity for item in items)

    # 🧾 Create Order
    order = Order.objects.create(
        user=request.user,
        total_amount=total
    )

    # 📦 Create Order Items
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    # 🧹 Clear Cart
    items.delete()

    return redirect('order_success')

def order_success(request):
    return render(request, 'order_success.html')
