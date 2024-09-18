from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from material.models import Material
from .serializers import MaterialSerializer

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