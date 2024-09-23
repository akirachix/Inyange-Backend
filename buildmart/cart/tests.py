from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from material.models import Material
from cart.models import UserCart
from cart.service import Cart
from decimal import Decimal

User = get_user_model()

class CartTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        
        # Create a test material
        self.material = Material.objects.create(
            material_id=1,
            material_name='Test Material',
            brand_name='Test Brand',
            price=Decimal('10.00'),
            quantity=100
        )
        
        # Mock the request and session
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.user = self.user
        self.request.session = self.client.session
        self.cart = Cart(self.request)  # Initialize the cart

    def tearDown(self):
        # Clean up any UserCart entries created during tests
        UserCart.objects.filter(user=self.user).delete()

    def test_add_item_to_cart(self):
        """Test adding an item to the cart."""
        material_data = {'id': self.material.material_id, 'price': str(self.material.price)}
        self.cart.add_item(material_data, quantity=2)
        
        # Check that the item is added correctly
        self.assertEqual(len(self.cart), 2)
        self.assertIn(str(self.material.material_id), self.cart.cart)
        self.assertEqual(self.cart.cart[str(self.material.material_id)]['quantity'], 2)
        self.assertEqual(Decimal(self.cart.cart[str(self.material.material_id)]['price']), self.material.price)

    def test_remove_item_from_cart(self):
        """Test removing an item from the cart."""
        material_data = {'id': self.material.material_id, 'price': str(self.material.price)}
        self.cart.add_item(material_data, quantity=2)
        self.cart.remove_item(self.material.material_id)
        
        # Check that the item is removed
        self.assertNotIn(str(self.material.material_id), self.cart.cart)
        self.assertEqual(len(self.cart), 0)

    def test_get_items(self):
        """Test retrieving all items from the cart."""
        material_data = {'id': self.material.material_id, 'price': str(self.material.price)}
        self.cart.add_item(material_data, quantity=2)
        
        # Check that the items are returned correctly
        items = list(self.cart.get_items())
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0][0], str(self.material.material_id))
        self.assertEqual(items[0][1]['quantity'], 2)

    def test_get_total_price(self):
        """Test calculating the total price of the cart."""
        material_data = {'id': self.material.material_id, 'price': str(self.material.price)}
        self.cart.add_item(material_data, quantity=2)
        
        # Check the total price
        self.assertEqual(self.cart.get_total_price(), Decimal('20.00'))

    # def test_clear_cart(self):
    #     """Test clearing the cart."""
    #     material_data = {'id': self.material.material_id, 'price': str(self.material.price)}
    #     self.cart.add_item(material_data, quantity=2)
    #     self.cart.clear()
        
    #     # Check that the cart is empty
    #     self.assertEqual(len(self.cart), 0)
    #     self.assertEqual(self.cart.get_total_price(), Decimal('0.00'))

    # def test_load_user_cart(self):
    #     """Test loading a user's cart from the database."""
    #     # Create a user cart; ensure to delete any existing carts first
    #     UserCart.objects.filter(user=self.user).delete()
    #     UserCart.objects.create(user=self.user, cart={
    #         str(self.material.material_id): {'quantity': 3, 'price': str(self.material.price)}
    #     })
        
        # Initialize a new cart to test loading
        # new_cart = Cart(self.request)
        
        # # Check that the cart is loaded correctly
        # self.assertEqual(new_cart.cart[str(self.material.material_id)]['quantity'], 3)

