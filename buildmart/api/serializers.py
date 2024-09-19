from rest_framework import serializers
from material.models import Material
from user.models import User
from django.core.exceptions import ValidationError


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'phone_number', 'first_name', 'last_name','user_role')
     
    
    def validate(self, data):
        
        if User.objects.filter(username=data['username']).exists():
            raise ValidationError({'username': 'Username already exists'})
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError({'email': 'Email already exists'})
        return data
    def create(self, validated_data):
       
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            role=validated_data['role']
        )
        return user



    
