import base64
import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import logging
from payments.utils import get_access_token
from payments.models import Payment
from payments.utils import query_mpesa_payment_status
# from payments.utils import generate_unique_checkout_request_id,generate_password
from payments.utils import generate_access_token, generate_password, generate_unique_checkout_request_id, query_mpesa_payment_status
from datetime import datetime
from django.http import JsonResponse
from .utils import generate_access_token
# Get the Mpesa token link
mpesa_token = settings.MPESA_ACCESS_TOKEN_LINK
# Set up logging
logger = logging.getLogger(__name__)
# payments/views.py
@csrf_exempt
def create_payment(request):
    checkout_request_id = request.POST.get('checkout_request_id')
    # Check if a payment with the same checkout_request_id already exists
    if Payment.objects.filter(checkout_request_id=checkout_request_id).exists():
        return JsonResponse({'error': 'Payment already exists with this checkout_request_id'}, status=400)
    # If no existing payment create a new payment
    payment = Payment.objects.create(
        checkout_request_id=checkout_request_id,
    )
    return JsonResponse({'success': 'Payment created'}, status=201)

@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data.get('phone_number')
            amount = data.get('amount')
            # Ensure the phone number and amount are provided
            if not phone_number or not amount:
                return JsonResponse({'error': 'Phone number and amount required'}, status=400)
            # Get Mpesa settings from Django settings
            logger.info("about to obtain codes from settings")
            shortcode = settings.MPESA_SHORTCODE
            passkey = settings.MPESA_PASSKEY
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            password = base64.b64encode(f'{shortcode}{passkey}{timestamp}'.encode()).decode('utf-8')
            mpesa_link = settings.MPESA_LINK
            logger.info(f'MPESA_LINK: {mpesa_link}')  # Log URL value
            # Ensure that MPESA_LINK is set in settings
            if not mpesa_link:
                return JsonResponse({'error': 'MPESA_LINK is not set in settings'}, status=500)
            # Generate the access token here
            # access_token = generate_access_token(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET)
            logger.info("about to generate access key")
            access_token = generate_access_token()
            if not access_token:
                return JsonResponse({'error': 'Failed to obtain access token'}, status=500)
            
            
            payload = {
                "BusinessShortCode": shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": 'https://buildmart.com/path',
                "AccountReference": "BuildMart",
                "TransactionDesc": "BuildMart Online Store"
            }
             # Generate a unique checkout_request_id
            checkout_request_id = generate_unique_checkout_request_id()
            # Save the initial payment record
            payment = Payment.objects.create(
                checkout_request_id=checkout_request_id,
                amount=amount,
                phone_number=phone_number,
                status='pending'
            )
            response = requests.post(
                mpesa_link,
                json=payload,
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
            )
            response_data = response.json()
            logger.info(f'STK push response: {response_data}')
            # Update the payment record with the checkout_request_id
            payment.checkout_request_id = response_data.get('CheckoutRequestID')
            payment.save()
            return JsonResponse(response_data)
        except Exception as e:
            logger.error(f'Error processing payment: {str(e)}')
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
# payments/views.py

@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            logger.debug("Received payload: %s", payload)
             # Extract important fields from the MPESA callback
            stk_callback = payload.get('Body', {}).get('stkCallback', {})
            result_code = stk_callback.get('ResultCode')
            result_desc = stk_callback.get('ResultDesc')
            checkout_request_id = stk_callback.get('CheckoutRequestID')
            transaction_id = stk_callback.get('TransactionID')  # Optional, may not be available
            payment = Payment.objects.filter(checkout_request_id=checkout_request_id).first()
            if payment:
                if result_code == 0:  # Payment successful
                    payment.status = 'completed'
                    payment.transaction_id = transaction_id
                    payment.save()
                    logger.info("Payment successful: %s", result_desc)
                    return JsonResponse({'status': 'success', 'message': 'Payment was successful'})
                else:
                    payment.status = 'failed'
                    payment.save()
                    logger.error("Payment failed: %s", result_desc)
                    return JsonResponse({'status': 'error', 'message': 'Payment failed'}, status=400)
            else:
                logger.error("Payment with CheckoutRequestID %s does not exist", checkout_request_id)
                return JsonResponse({'status': 'error', 'message': 'Payment record not found'}, status=404)
        except json.JSONDecodeError:
            logger.error("Invalid JSON payload")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error("Exception occurred: %s", str(e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    
    
@csrf_exempt
def check_payment_status_view(request):
    checkout_request_id = request.GET.get('checkout_request_id')
    if not checkout_request_id:
        return JsonResponse({'status': 'error', 'message': 'Missing CheckoutRequestID'}, status=400)
    # Query the payment status
    result = query_mpesa_payment_status(checkout_request_id)
    # Check if the payment exists in the database
    payment = Payment.objects.filter(checkout_request_id=checkout_request_id).first()
    if payment:
        # Update the existing payment record
        payment.status = result.get('status')
        payment.message = result.get('message')
        payment.save()
    else:
        # Create a new payment record
        Payment.objects.create(
            checkout_request_id=checkout_request_id,
            status=result.get('status'),
            message=result.get('message')
        )
    return JsonResponse(result)