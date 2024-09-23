from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from order.models import Order
from .models import Cart 


class CompletePurchaseView(APIView):
    
    
    permission_classes = [IsAuthenticated]  
    
    def post(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return HttpResponse("Your cart is empty.")
        if not cart.get_items():
            return HttpResponse("Your cart is empty.")
        cart_items = cart.get_items()
        print("Cart Items Debug:", cart_items) 
        try:
            order = Order.objects.create(
                homeowner=request.user,
                cart_data=cart_items,  
                order_date=timezone.now(),
                status="Pending",
                supplier=None
            )
        except Exception as e:
            return HttpResponse(f"An error occurred while creating the order: {str(e)}")
        cart.clear()
        return redirect('order_confirmation', order_id=order.id)
    def get(self, request, *args, **kwargs):
        return HttpResponse("Invalid request method.", status=405)
