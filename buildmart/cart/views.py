from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils import timezone
from order.models import Order
from cart.service import Cart

def complete_purchase(request):
    cart = Cart(request)
    
    if not cart.get_items():
        return HttpResponse("Your cart is empty.")
    
    cart_items = cart.get_items()
    print("Cart Items Debug:", cart_items)  # Debugging statement

    try:
        order = Order.objects.create(
            homeowner=request.user,
            cart_data=cart_items,  # Ensure this is the correct data format
            order_date=timezone.now(),
            status="Pending",
            supplier=None
        )
    except Exception as e:
        return HttpResponse(f"An error occurred while creating the order: {str(e)}")

    cart.clear()
    return redirect('order_confirmation', order_id=order.id)
