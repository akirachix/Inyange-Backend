from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from material.models import Material
from .serializers import MaterialSerializer
from .serializers import OrderSerializer
from order.models import Order
from .serializers import UserSerializer
from cart.service import Cart
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from decimal import Decimal
from django.shortcuts import get_object_or_404
from cart.service import Cart
import logging
logger = logging.getLogger(__name__)

User = get_user_model()


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
    def get(self, request):
        category = request.query_params.get('category', None)  # Filter by category
        brand = request.query_params.get('brand', None)  # Filter by brand
        min_price = request.query_params.get('min_price', None)  # Minimum price
        max_price = request.query_params.get('max_price', None)  # Maximum price
        sort_by = request.query_params.get('sort', 'price')  # Sorting option (default to price)

        queryset = Material.objects.all()

        if category:
            queryset = queryset.filter(category_name=category)
        if brand:
            queryset = queryset.filter(brand_name=brand)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        if sort_by in ['price', '-price', 'material_name', '-material_name']:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('price')  # Default sorting

        serializer = MaterialSerializer(queryset, many=True)
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
            token, created = Token.objects.get_or_create(user=user)
            if created:
                logger.info(f'Token created for user: {email}')
            else:
                logger.info(f'Token retrieved for user: {email}')
                
            response = {
                'success': True,
                'email': user.email,
                'token': token.key
            }
            return Response(response, status=status.HTTP_200_OK)

        logger.error(f'Login failed for user: {email}')
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
                
    
class OrderListView(APIView):
    """
    List all orders or create a new order.
    """
    def get(self, request, format=None):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrderDetailView(APIView):
    """
    Retrieve, update or delete a specific order by ID.
    """
    def get(self, request, id, format=None):
        try:
            order = Order.objects.get(order_id=id)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        try:
            order = Order.objects.get(order_id=id)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        try:
            order = Order.objects.get(order_id=id)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class CartListView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request, format=None):
        user = request.user
        try:
            cart = Cart(request)
            cart_data = []
            cart_total_price = Decimal('0.00')
            
            print(f"Cart before processing: {cart.cart}")
            for item_id, item in cart.get_items():
                material_name = item.get('material_name')
                brand_name = item.get('brand_name')
                if not material_name or not brand_name:
                    logger.error(f"Missing material_name or brand_name in cart item: {item}")
                    continue  
                materials = Material.objects.filter(material_name=material_name, brand_name=brand_name)
                if materials.exists():
                    material_obj = materials.first()
                    total_price = Decimal(item['price']) * item['quantity']
                    product = {
                        "id": material_obj.material_id,
                        "name": material_obj.material_name,
                        "description": material_obj.description,
                        "price": str(material_obj.price),
                        "image": material_obj.image.url if material_obj.image else None,
                        "is_available": material_obj.quantity > 0,
                        "created_at": material_obj.created_at,
                        "modified_at": material_obj.modified_at,
                    }
                    cart_data.append({
                        "product": product,
                        "quantity": item['quantity'],
                        "total_price": str(total_price),
                        "remove": True
                    })
                    cart_total_price += total_price
                else:
                    logger.warning(f"Material not found for {material_name} by {brand_name}.")
                    cart_data.append({
                        "error": f"Material not found: {material_name} by {brand_name}",
                        "quantity": item['quantity'],
                    })
            return Response({
                "data": cart_data,
                "cart_total_price": str(cart_total_price)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error retrieving cart: %s", str(e))
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def post(self, request, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication credentials required."}, status=status.HTTP_401_UNAUTHORIZED)
        items = request.data.get('items', [])
        if not items or not isinstance(items, list):
            return Response({"error": "Invalid request. 'items' should be a list of item objects."}, status=status.HTTP_400_BAD_REQUEST)
        cart = Cart(request)
        added_items = [] 
        errors = [] 
        for item in items:
            material_name = item.get('material_name')
            brand_name = item.get('brand_name')
            price = item.get('price', '0.00')
            quantity = item.get('quantity', 1)
            override_quantity = item.get('override_quantity', False)
            if not material_name or not brand_name:
                error_message = f"Missing required fields: 'material_name' or 'brand_name' for item: {item}"
                logger.error(error_message)
                errors.append({"error": error_message})
                continue 
            try:
                material_obj = None
                materials = Material.objects.filter(material_name=material_name, brand_name=brand_name)
                if not materials.exists():
                    error_message = f"Material not found: {material_name} by {brand_name}."
                    logger.error(error_message)
                    errors.append({"error": error_message})
                    continue  
                if materials.count() > 1:
                    error_message = f"Multiple materials found for name: {material_name} and brand: {brand_name}."
                    logger.warning(error_message)
                    errors.append({"error": error_message})
                    continue 
                material_obj = materials.first()
            except Exception as e:
                error_message = f"Error finding material: {str(e)} for item: {item}"
                logger.error(error_message)
                errors.append({"error": error_message})
                continue  
            if material_obj is None:
                error_message = "Unexpected error: Material object is None after filtering."
                logger.error(error_message)
                errors.append({"error": error_message})
                continue  
            try:
                cart.add_item({
                    'id': material_obj.material_id,  
                    'name': material_obj.material_name,
                    'price': price,
                    'quantity': quantity,
                    }, override_quantity=override_quantity)
                added_items.append({
                    'id': material_obj.material_id,
                    'name': material_name,
                    'price': price,
                    'quantity': quantity
                    })
            except Exception as e:
                error_message = f"Failed to add item: {material_name} by {brand_name}. Reason: {str(e)}"
                logger.error(error_message)
                errors.append({"error": error_message})
                continue  
            cart_items = list(cart.get_items())
            cart_total_price = str(cart.get_total_price())  
            item_count = len(cart)  
            material_ids = [item_id for item_id, _ in cart_items]
            materials = Material.objects.filter(material_id__in=material_ids)
            material_dict = {str(material.material_id): material.material_name for material in materials}
            formatted_cart_items = [
                {
                    "material_id": item_id,
                    "material_name": material_dict.get(item_id, "Unknown"),  
                    "quantity": item_data["quantity"],
                    "price": item_data["price"],
                    "user_id": item_data["user_id"]
                    }
                for item_id, item_data in cart_items
                ]
            
            cart_details = {
                "cart_items": formatted_cart_items,
                "cart_total_price": cart_total_price,
                "item_count": item_count
                }
            response = {
                "message": "Items processed.",
                "cart_details": cart_details,
                "errors": errors  
                }
        return Response(response, status=status.HTTP_201_CREATED)
        
        
        
        
   