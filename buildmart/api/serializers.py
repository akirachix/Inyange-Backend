from rest_framework import serializers
from material.models import Material
from order.models import Order
from user.models import User
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token



class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'
        
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'phone_number', 'first_name', 'last_name','user_role')
        extra_kwargs = {'password':{'write_only': True}}
     
    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise ValidationError({'username': 'Username already exists'})
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError({'email': 'Email already exists'})
        return data
    def create(self, validated_data):
        if User.objects.filter(username=validated_data['username']).exists():
            raise ValidationError({"username": "This username is already taken."})

        if User.objects.filter(email=validated_data['email']).exists():
            raise ValidationError({"email": "This email is already registered."})

        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user






    
