from .models import Cart,CartItem
from django.contrib.auth.decorators import login_required



def cart_quantity(request):
    if request.user.is_authenticated:
        cart,created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()
        total_quantity = sum(item.quantity for item in items)
    else:
        total_quantity=0

    return { 'total_quantity': total_quantity }