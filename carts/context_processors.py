from .models import Cart, CartItem
from .views import _cart_session_key


def cart_item_count(requests):
    cart = Cart.objects.get(cart_id=_cart_session_key(requests))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    total_cart_items = cart_items.count()
    return dict(total_cart_items=total_cart_items)