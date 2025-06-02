from .models import Cart, CartItem
from .views import _cart_session_key


def cart_item_count(requests):
    if 'admin' in requests.path:
        return {}
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_session_key(requests))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            total_cart_items = cart_items.count()
        except Cart.DoesNotExist:
            total_cart_items = 0
    return dict(total_cart_items=total_cart_items)