from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.http import HttpResponse


# Create your views here.

# Generate a unique cart session key
# for each user
def _cart_session_key(request):
    cart_session_key = request.session.session_key
    if not cart_session_key:
        cart_session_key = request.session.create()
    return cart_session_key


# Add product to cart
# and create a cart if it doesn't exist
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_session_key(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_session_key(request)
        )
    cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
        
    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_session_key(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_session_key(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

# def add_cart_item(request, product_id):
#     cart = Cart.objects.get(cart_id = _cart_session_key(request))
#     product = get_object_or_404(Product, id=product_id)
#     cart_item = CartItem.objects.get(product=product, cart=cart)
#     cart_item.quantity += 1
#     cart_item.save()
#     return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_session_key(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        # Debug prints
        print('Cart ID:', cart.cart_id)
        print('Total Cart Items:', cart_items.count())
        
        total_cart_items = cart_items.count()
        
        for cart_item in cart_items:
            print('Product:', cart_item.product.product_name)
            print('Quantity:', cart_item.quantity)
            
            
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except Cart.DoesNotExist:
        pass
    tax = (2 * total) / 100
    grand_total = total + tax
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'total_cart_items': total_cart_items,
        'is_cart_page' : True,
    }
    return render(request, 'store/cart.html', context)
