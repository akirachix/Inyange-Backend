
from django.urls import path
from . import views
    
urlpatterns = [
    path("login/", views.login, name="login"),
    path("callback/", views.callback, name="callback"),
    path("logout/", views.logout, name="logout"),
    path("login_sso/", views.loginSSO, name="login_sso"),
    path("", views.index, name="index"),
   
]





