from decimal import Decimal
from django.conf import settings
from api.serializers import MaterialSerializer 
from material.models import Material
from order.models import Order  



class Cart:
    def __init__(self, request):
         """
        Initializes the Cart object. It checks if the session has a cart already.
        If not, it creates a new cart and stores it in the session.
        """
         self.session = request.session
         self.homeowner_id = request.session.get('homeowner_id')  # Retrieve homeowner_id from the session
         self.cart = self.session.get(settings.CART_SESSION_ID, {})

        
        # Try to retrieve the cart from session, or create a new empty cart if it doesn't exist
         cart = self.session.get('cart')
         if not cart:
            # Create an empty cart in session if it doesn't exist
            cart = self.session['cart'] = {}
         self.cart = cart


    def add(self, material, quantity=1, override_quantity=False):
        material_id = material.get('id')
        material_name = material.get('name')
    
    # Handle cases where id is missing but name is provided
        if not material_id and material_name:
           try:
            # Fetch material object using name
                material_obj = Material.objects.get(material_name=material_name)
                material_id = material_obj.material_id
           except Material.DoesNotExist:
                raise Exception("Material not found")
    
        if material_id:
        # Existing logic to handle adding to cart
           if material_id in self.cart:
               if override_quantity:
                  self.cart[material_id]['quantity'] = quantity
               else:
                  self.cart[material_id]['quantity'] += quantity
           else:
               self.cart[material_id] = {'quantity': quantity, 'price': material.get('price', '0.00'), 'homeowner_id': self.homeowner_id}
        
           self.save()
        else:
             raise Exception("Material ID or Name is required")
        
    def save(self):
        """
        Marks the session as modified to ensure that the cart is saved when it is updated.
        """
        self.session.modified = True
        
        
    def remove(self, material):
        """
        Removes a material from the cart.
        
        Parameters:
        material: The material to be removed from the cart.
        """
        material_id = str(material["id"])  # Convert the material ID to a string
        if material_id in self.cart:
            del self.cart[material_id]  # Remove the material from the cart
            self.save()  # Save the session to persist changes
            

    def __iter__(self):
        material_ids = self.cart.keys()
        materials = Material.objects.filter(material_id__in=material_ids)
    
        cart = self.cart.copy()
        for material in materials:
          cart[str(material.material_id)]["material"] = MaterialSerializer(material).data

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            item["homeowner_id"] = self.homeowner_id  # Add homeowner_id to each item
            yield item
            
            
    def get_items(self):
         return list(self.cart.values())

    def __len__(self):
        """
        Returns the total number of items in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())  # Sum all quantities in the cart

    def get_total_price(self):
        """
        Returns the total price for all items in the cart by summing up their individual total prices.
        """
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    def clear(self):
        """
        Clears all items from the cart by deleting it from the session.
        """
        self.session.pop[settings.CART_SESSION_ID, None]  # Remove the cart from the session
        self.session.modified = True
        
        
      
   