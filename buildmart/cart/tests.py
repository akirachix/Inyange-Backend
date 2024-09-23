from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from material.models import Material
from cart.service import Cart

User = get_user_model()

class CartTestCase(TestCase):
    def setUp(self):
        # Create a user and log in
        self.user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
        self.client.login(username='testuser', password='testpass')

        # Use RequestFactory to create a request object
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.user = self.user
        self.request.session = self.client.session

        # Initialize the cart
        self.cart = Cart(self.request)

        # Create a test material
        self.material = Material.objects.create(
            material_name='Test Material',
            brand_name='Test Brand',
            price='10.00',
            quantity=1
        )

    def test_add_item(self):
        self.cart.add_item({'id': self.material.id}, quantity=2)
        self.assertIn(str(self.material.id), self.cart.cart)
        self.assertEqual(self.cart.cart[str(self.material.id)]['quantity'], 2)
