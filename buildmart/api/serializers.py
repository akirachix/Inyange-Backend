from rest_framework import serializers
from material.models import Material
from order.models import Order
from supplier.models import Supplier
from homeowner.models import Homeowner



class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"
        
        
class OrderSerializer(serializers.ModelSerializer):  
    class Meta:
        model=Order
        fields="__all__"
        
        
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        
        
class HomeownerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homeowner
        fields = '__all__'
        
        
