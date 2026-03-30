from .models import Cart, CartItem
from django.db.models import Sum

def cart_count(request):
    # Check if user is logged in
    if request.user.is_authenticated:

        # Get user's cart
        cart = Cart.objects.filter(user=request.user).first()

        if cart:
            # Calculate total quantity (optimized query)
            count = CartItem.objects.filter(cart=cart).aggregate(
                total=Sum('quantity')
            )['total'] or 0

            return {'cart_count': count}

    # Default if no cart or not logged in
    return {'cart_count': 0}
