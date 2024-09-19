import base64
from datetime import datetime
import requests
from payments.auth import get_access_token  # Ensure this function is correctly implemented
import os 
import uuid
import logging
from requests.auth import HTTPBasicAuth
from django.conf import settings
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

def generate_unique_checkout_request_id():
    return str(uuid.uuid4())
    
def generate_password(shortcode, passkey):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(f'{shortcode}{passkey}{timestamp}'.encode()).decode('utf-8')
    return password 


def generate_access_token():
    logging.info(f"MPESA_CONSUMER_KEY: {settings.MPESA_CONSUMER_KEY}")
    logging.info(f"MPESA_CONSUMER_SECRET: {settings.MPESA_CONSUMER_SECRET}")
    logging.info(f"MPESA_ACCESS_TOKEN_LINK: {settings.MPESA_ACCESS_TOKEN_LINK}")
    # # Load credentials from settings
    token_url = settings.MPESA_ACCESS_TOKEN_LINK
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET

    # Debugging: Print or log the values
    print(f"Token URL: {token_url}")
    print(f"Consumer Key: {consumer_key}")
    print(f"Consumer Secret: {consumer_secret}")

    # Ensure that the values exist
    if not all([token_url, consumer_key, consumer_secret]):
        raise ValueError("MPESA_ACCESS_TOKEN_LINK, MPESA_CONSUMER_KEY, or MPESA_CONSUMER_SECRET is not set in settings.")

    # Make request to get access token
    response = requests.get(token_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        raise Exception(f"Error generating access token: {response.status_code} - {response.text}")


# Function to generate a timestamp
def get_timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')

# Function to query the status of an M-Pesa payment using the checkout request ID
def query_mpesa_payment_status(checkout_request_id):
    try:
        access_token = get_access_token()
        api_url = os.getenv('MPESA_QUERY_URL', 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query') 
        
    # Retrieve shortcode and passkey from environment variables

        shortcode = os.getenv('MPESA_SHORTCODE')
        passkey = os.getenv('MPESA_PASSKEY')
        
        if not all([access_token, shortcode, passkey]):
            raise ValueError("Missing one or more environment variables.")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        
         # Generate the password required for the API request using the shortcode and passkey
        password = generate_password(shortcode, passkey)
        
        payload = {
            "BusinessShortCode": shortcode,
            "Password": password,
            "Timestamp": get_timestamp(),
            "CheckoutRequestID": checkout_request_id,
        }

        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        result = response.json()
        result_code = result.get('ResultCode')

        if result_code == "0":
            return {
                'status': 'success',
                'message': 'Payment was successful',
                'data': result
            }
        else:
            return {
                'status': 'error',
                'message': 'Payment failed or is pending',
                'data': result
            }
    except requests.RequestException as e:
        logger.error(f"Request error: {e}")
        return {
            'status': 'error',
            'message': 'Failed to query payment status',
            'data': str(e)
        }
    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            'status': 'error',
            'message': 'An unexpected error occurred',
            'data': str(e)
        }

        