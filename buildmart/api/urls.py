from django.urls import path
from .views import UserListView
from .views import LoginListView
from .views import RegisterView


urlpatterns = [
    path("user/", UserListView.as_view(), name="user_list_view"),
    path("login/", LoginListView.as_view(), name="login_list_view"),
    path("register/", RegisterView.as_view(), name="register_list_view"),


]