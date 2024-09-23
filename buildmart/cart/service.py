"""Module to handle cart operations for the application."""

from decimal import Decimal
from django.conf import settings
from django.contrib.auth import get_user_model
from api.serializers import MaterialSerializer
from material.models import Material
from cart.models import UserCart

User = get_user_model()  

class Cart:
    """Handles the user's shopping cart functionality."""
    
    def __init__(self, request):
        """Initializes the cart."""
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID, {})
        self.user = request.user if request.user.is_authenticated else None
        
        
        if not isinstance(self.cart,dict):
            self.cart={}
        if not self.cart:
            self.cart={}
            
        if self.user:
            self.load_user_cart()
            
    def load_user_cart(self):
        """Loads the user's cart from the database."""
        if self.user and self.user.is_authenticated:
            # Use the UserCart model to fetch or create a cart for the user
            user_cart, created = UserCart.objects.get_or_create(user=self.user)
            if created:
                self.cart = {}  # If no cart exists, initialize an empty cart
            else:
                self.cart = user_cart.cart  # Load the cart from the database
                
    def add_item(self, material, quantity=1, override_quantity=False):
        material_id = str(material.get('id'))  # Convert material ID to string to use as key
        if not material_id:
            raise ValueError("Material ID is required")
        
        if material_id in self.cart:
            if override_quantity:
                self.cart[material_id]['quantity'] = quantity
            else:
                self.cart[material_id]['quantity'] += quantity
        else:
            self.cart[material_id] = {
                'quantity': quantity,
                'price': material.get('price', '0.00'),
                'user_id': self.user.id if self.user else None
        }
        self.save()
        print(f"Cart after adding item: {self.cart}")  # Debug: print cart state after adding item        

    def save(self):
        """Saves the current cart session."""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        print(f"Cart saved to session: {self.session[settings.CART_SESSION_ID]}")

    def remove_item(self, material_id):
        """Removes an item from the cart."""
        if str(material_id) in self.cart:
            del self.cart[str(material_id)]
            self.save()

    def __iter__(self):
        """Iterates over the items in the cart."""
        material_ids = self.cart.keys()
        materials = Material.objects.filter(material_id__in=material_ids)
        cart = self.cart.copy()
        for material in materials:
            cart[str(material.material_id)]["material"] = MaterialSerializer(material).data
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item     
              
    def get_items(self):
        """Returns all items in the cart."""
        print(f"Cart items: {self.cart}")
        return self.cart.items()

    def __len__(self):
        """Returns the total number of items in the cart."""
        return sum(item["quantity"] for item in self.cart.values())
    
    def get_total_price(self):
        """Calculates the total price of the cart."""
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())
    
    def clear(self):
        """Clears the cart session."""
        del self.session[settings.CART_SESSION_ID]
        self.save()
