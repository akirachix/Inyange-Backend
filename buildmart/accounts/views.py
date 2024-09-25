
import json
import logging
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as django_login
from urllib.parse import quote_plus, urlencode
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from user.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"http://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)
logger = logging.getLogger(__name__)


@csrf_exempt
def login(request):
    """
    Redirect the user to the Auth0 login page.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        logger.info(f"Login attempt for username: {username}")
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            django_login(request, user)
            logger.info (f"User {username} logged in sucessfully.")
            
            return JsonResponse({'status':'success','message':'Logged in successfully!'}, status=200)
        else:
            logger.warning(f"Failed login attempt for username: {username}")

            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def login(request):
    """
    Redirect the user to the Auth0 login page.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        logger.info(f"Login attempt for username: {username}")
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            django_login(request, user)
            logger.info (f"User {username} logged in sucessfully.")
            
            return JsonResponse({'status':'success','message':'Logged in successfully!'}, status=200)
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            return JsonResponse({'status':'error', 'message':'Invalid credentials'}, status=400)thenticate(username=username, password=password)
        if user is not None and user.is_active:
            django_login(request, user)
            logger.info (f"User {username} logged in sucessfully.")
            
            return JsonResponse({'status':'success','message':'Logged in successfully!'}, status=200)
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            return JsonResponse({'status':'error', 'message':'Invalid credentials'}, status=400)

@csrf_exempt
def loginSSO(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


@csrf_exempt
def callback(request):
    """
    Handle the callback from Auth0 after user authentication.
    """
    state = request.GET.get('state')
    logger.debug(f"Callback state: {state}")
    
    try:
        token = oauth.auth0.authorize_access_token(request)

        request.session["user"] = token

        return redirect(request.build_absolute_uri(reverse("index")))
    except Exception as e:
        logger.error(f"Error during OAuth callback: {e}")
        return JsonResponse({'status':'error','message':'Failed to authorize'}, status=400)



@csrf_exempt
def logout(request):
    """
    Log the user out by clearing the session and redirecting to Auth0 logout URL.
    """
    request.session.clear()
    if request.method =='POST':
        return JsonResponse({'status':'sucess','message':'User logged out sucesssfully'}, status=200)
    else:
        return redirect(
            f"http://{settings.AUTH0_DOMAIN}/v2/logout?" + urlencode(
        {
            "returnTo": request.build_absolute_uri(reverse("index")),
            "client_id": settings.AUTH0_CLIENT_ID,
        },
        quote_via=quote_plus,
    ),
  )


def check_existing_email(email):
    """
    Check if a user with the given email address already exists.
    """
    return User.objects.filter(email=email).exists()


def index(request):
    """
    Render the index page if the user is logged in; otherwise, redirect to login.
    """
    user = request.session.get("user")

    if not user:
        return redirect(reverse("login"))

    email = user["userinfo"].get("email")

    if not email:
        return HttpResponse("Email not passed in the token.")

    if not check_existing_email(email):
        return HttpResponse("User does not exist.")

    return render(
        request,
        "accounts/index.html",
        context={
            "user_authenticated":request.user.is_authenticated,
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )


@csrf_exempt
def test_callback_csrf_warning(self):
    response = self.client.get(self.callback_url)
    self.assrtIn(b'CSRF Warning! State not equal in request and response.', response.content)

    

