
import requests
from django.conf import settings

def get_access_token():
    url = settings.MPESA_ACCESS_TOKEN_LINK
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(
            f'{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}'.encode('utf-8')
        ).decode('utf-8')
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        response.raise_for_status()