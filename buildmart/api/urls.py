from django.urls import path

from .views import MaterialDetailView
from .views import MaterialListView
from .views import CartListView
from .views import OrderDetailView
from .views import OrderListView
from .views import SupplierDetailView
from .views import SupplierListView
from .views import HomeownerDetailView
from .views import HomeownerListView

urlpatterns = [
    path("materials/", MaterialListView.as_view(), name = "material_list_view"),
    path("material/<int:id>/", MaterialDetailView.as_view(), name="material_detail_view"),
    path('cart/', CartListView.as_view(), name='cart'),
    path("orders/", OrderListView.as_view(), name = "order_list_view"),
    path("order/<int:id>/", OrderDetailView.as_view(), name = "order_detail_view"),  
    path("homeowners/", HomeownerListView.as_view(), name = "homeowner_list_view"),
    path("homeowner/<int:id>/", HomeownerDetailView.as_view(), name = "homeowner_detail_view"),
    path("suppliers/", SupplierListView.as_view(), name = "supplier_list_view"),
    path("supplier/<int:id>/", SupplierDetailView.as_view(), name = "supplier_detail_view"),
]