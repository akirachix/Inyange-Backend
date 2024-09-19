from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from material.models import Material
from .serializers import MaterialSerializer

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer

# Create your views here.

class MaterialListView(APIView):
    def get(self, request):
        materials = Material.objects.all()
        serializer = MaterialSerializer(materials, many = True)

        return Response(serializer.data)
    
    def post(self, request):
        serializer = MaterialSerializer(data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


class MaterialDetailView(APIView):
    def get(self, request, id):
        try:
            material = Material.objects.get(material_id=id)
        except Material.DoesNotExist:
            return Response({'error': f'Material with id {id} not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MaterialSerializer(material)
        return Response(serializer.data)
    
    def put(self, request, id):
        try:
            material = Material.objects.get(material_id=id)
        except Material.DoesNotExist:
            return Response({'error': f'Material with id {id} not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MaterialSerializer(material, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

import logging
logger = logging.getLogger(__name__)

User = get_user_model()

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.pop('password')
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password

            user = User.objects.create(**serializer.validated_data)
            logger.info(f'User registered successfully: {user.email}')
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

        logger.error(f'User registration failed: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginListView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        allowed_fields = {'email', 'password'}
        provided_fields = set(request.data.keys())
        extra_fields = provided_fields - allowed_fields
        
        if extra_fields:
            invalid_fields = ', '.join(extra_fields)
            logger.warning(f'Login attempt with unexpected fields: {invalid_fields}')
            return Response({'error': f'Invalid fields provided: {invalid_fields}'}, status=status.HTTP_400_BAD_REQUEST)

        if not email or not password:
            logger.warning('Login attempt with missing email or password')
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if user is not None:
            logger.info(f'User logged in successfully: {email}')
            return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)

        logger.error(f'Login failed for user: {email}')
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
