from django.urls import path

from .views import MaterialDetailView
from .views import MaterialListView

urlpatterns = [
    path("materials/", MaterialListView.as_view(), name = "material_list_view"),
    path("material/<int:id>/", MaterialDetailView.as_view(), name="material_detail_view"),
]