from rest_framework import serializers
from material.models import Material
from order.models import Order



class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"
        
        
class OrderSerializer(serializers.ModelSerializer):  
    class Meta:
        model=Order
        fields="__all__"
        
        

        
