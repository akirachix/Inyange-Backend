from django.test import TestCase
from .models import Material
import unittest

from django.core.exceptions import ValidationError
class MaterialModelTest(TestCase):
    def setUp(self):
        self.material = Material.objects.create(
            category_name='Building materials',
            material_name='Cement',
            brand_name='BrandX',
            description='High-quality cement',
            price=50.00,
            quantity=100
        )
    def test_material_creation(self):
        material = self.material
        self.assertIsInstance(material, Material)
        self.assertEqual(str(material), 'Cement High-quality cement')
        self.assertEqual(material.category_name, 'Building materials')
        self.assertEqual(material.material_name, 'Cement')
        self.assertEqual(material.brand_name, 'BrandX')
        self.assertEqual(material.description, 'High-quality cement')
        self.assertEqual(material.price, 50.00)
        self.assertEqual(material.quantity, 100)
    def test_category_choices(self):
        categories = dict(Material.CATEGORY_CHOICES)
        self.assertEqual(len(categories), 3)
        self.assertIn('Building materials', categories.values())
        self.assertIn('Finishing materials', categories.values())
        self.assertIn('Hardware and tools', categories.values())
    def test_material_price(self):
        self.assertGreater(self.material.price, 0)
    def test_material_quantity(self):
        self.assertEqual(self.material.quantity, 100)
    def test_material_update(self):
        self.material.price = 60.00
        self.material.quantity = 120
        self.material.save()
        updated_material = Material.objects.get(material_id=self.material.material_id)
        self.assertEqual(updated_material.price, 60.00)
        self.assertEqual(updated_material.quantity, 120)
    def test_negative_quantity(self):
        with self.assertRaises(ValidationError):
            material = Material(
                category_name='Building materials',
                material_name='Cement',
                brand_name='BrandX',
                description='High-quality cement',
                price=50.00,
                quantity=-10
            )
            material.full_clean()
    def test_exceeding_description_length(self):
        with self.assertRaises(ValidationError):
            material = Material(
                category_name='Building materials',
                material_name='Cement',
                brand_name='BrandX',
                description='A' * 101,
                price=50.00,
                quantity=100
            )
            material.full_clean()
        if __name__ == "__main__":
         unittest.main()