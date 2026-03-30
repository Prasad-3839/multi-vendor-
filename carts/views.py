from django.shortcuts import render,get_object_or_404, redirect

# Create your views here.
from .models import Cart, CartItem
from products.models import Product


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    product = get_object_or_404(
        Product,
        id=product_id,
        vendor__is_approved=True  # 🔒 important
    )

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('carts:cart')


def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = Cart.objects.filter(user=request.user).first()
    items = CartItem.objects.filter(cart=cart) if cart else []

    total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'cart/cart.html', {
        'items': items,
        'total': total
    })


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('carts:cart')


def update_quantity(request, item_id):
    from .models import CartItem
    from django.shortcuts import get_object_or_404, redirect

    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    action = request.GET.get('action')

    if action == 'increase':
        item.quantity += 1

    elif action == 'decrease':
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
            return redirect('carts:cart')  # use namespace if applied

    item.save()
    return redirect('carts:cart')
