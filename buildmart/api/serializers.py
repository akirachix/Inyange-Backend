from rest_framework import serializers
from material.models import Material
from user.models import User
from django.core.exceptions import ValidationError


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'







    
