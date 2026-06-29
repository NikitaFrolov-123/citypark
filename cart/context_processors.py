from .cart import Cart


def cart_context(request):
    cart = Cart(request)
    return {
        'cart_count': len(cart),
        'cart_total_price': cart.get_total_price(),
    }