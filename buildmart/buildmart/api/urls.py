from django.urls import path
from .views import UserListView, LoginListView, RegisterView
from .views import MaterialDetailView, MaterialListView

urlpatterns = [
    path("user/", UserListView.as_view(), name="user_list_view"),
    path("login/", LoginListView.as_view(), name="login_list_view"),
    path("register/", RegisterView.as_view(), name="register_list_view"),
    path("materials/", MaterialListView.as_view(), name="material_list_view"),
    path("material/<int:id>/", MaterialDetailView.as_view(), name="material_detail_view"),
]
