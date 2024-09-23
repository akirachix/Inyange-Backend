from django.test import TestCase
from material.models import Material
from .models import Order
from django.utils import timezone


class OrderModelTest(TestCase):
    def setUp(self):
        self.material = Material.objects.create(
            category_name='Building materials',
            material_name='Test Material',
            brand_name='Test Brand',
            description='A material for testing purposes',
            price=10.00,
            quantity=100,
            image=None  
        )
        self.order = Order.objects.create(
            material=self.material,
            order_date=timezone.now(),  
            status='Pending',
            cart_data={'item1': 2, 'item2': 5}
        )
    def test_order_creation(self):
        self.assertEqual(self.order.material, self.material)
        self.assertEqual(self.order.status, 'Pending')
        self.assertEqual(self.order.cart_data, {'item1': 2, 'item2': 5})
    def test_order_string_representation(self):
        expected_str = f"{self.order.order_date} Pending"
        self.assertEqual(str(self.order), expected_str)
    def test_order_auto_id(self):
        order2 = Order.objects.create(
            material=self.material,
            order_date=timezone.now(),
            status='Completed',
            cart_data={'item1': 1}
        )
        self.assertEqual(order2.order_id, self.order.order_id + 1)
   