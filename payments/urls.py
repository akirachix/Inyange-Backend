from django.urls import path
from .views import process_payment, mpesa_callback, check_payment_status_view

urlpatterns = [
    path('process_payment/', process_payment, name='process_payment'),
    path('mpesa_callback/', mpesa_callback, name='mpesa_callback'),
    path('check_payment_status/', check_payment_status_view, name='check_payment_status'),
]