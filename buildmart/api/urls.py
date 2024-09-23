from django.urls import path
from .views import MaterialDetailView
from .views import MaterialListView
from .views import UserListView
from .views import LoginListView
from .views import RegisterView
from .views import OrderDetailView
from .views import OrderListView
from .views import CartListView
from rest_framework.authtoken import views
from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns = [
    path("materials/", MaterialListView.as_view(), name = "material_list_view"),
    path("material/<int:id>/", MaterialDetailView.as_view(), name="material_detail_view"),
    path("user/", UserListView.as_view(), name="user_list_view"),
    path("login/", LoginListView.as_view(), name="login_list_view"),
    path("register/", RegisterView.as_view(), name="register_list_view"),
    path("orderdetails/", OrderListView.as_view(), name = "order_list_view"),
    path("orderdetail/<int:id>/", OrderDetailView.as_view(), name = "order_detail_view"), 
    path('order/', CartListView.as_view(), name='order'),
    path('api-token-auth/', views.obtain_auth_token),
    path('generate_token/', ObtainAuthToken.as_view(), name='generate_token'),
    

]