from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Material

class MaterialModelTest(TestCase):
    def setUp(self):
        # Create a sample Material instance to use in the tests
        self.material = Material.objects.create(
            hardware_name='Hardware Store A',
            category_name='Building materials',
            material_name='Cement',
            brand_name='BrandX',
            description='High-quality cement',
            price=50.00,
            quantity=100
        )

    def test_material_creation(self):
        """Test that a Material instance is created successfully."""
        material = self.material
        self.assertIsInstance(material, Material)
        self.assertEqual(str(material), 'Cement High-quality cement')
        self.assertEqual(material.hardware_name, 'Hardware Store A')
        self.assertEqual(material.category_name, 'Building materials')
        self.assertEqual(material.material_name, 'Cement')
        self.assertEqual(material.brand_name, 'BrandX')
        self.assertEqual(material.description, 'High-quality cement')
        self.assertEqual(material.price, 50.00)
        self.assertEqual(material.quantity, 100)

    def test_category_choices(self):
        """Test that category choices include valid options."""
        categories = dict(Material.CATEGORY_CHOICES)
        self.assertEqual(len(categories), 3)
        self.assertIn('Building materials', categories.values())
        self.assertIn('Finishing materials', categories.values())
        self.assertIn('Hardware and tools', categories.values())

    def test_material_price_positive(self):
        """Test that the price of a material is greater than zero."""
        self.assertGreater(self.material.price, 0)

    def test_material_quantity(self):
        """Test that quantity is set correctly."""
        self.assertEqual(self.material.quantity, 100)

    def test_material_update(self):
        """Test updating a Material instance."""
        self.material.price = 60.00
        self.material.quantity = 120
        self.material.save()
        updated_material = Material.objects.get(material_id=self.material.material_id)
        self.assertEqual(updated_material.price, 60.00)
        self.assertEqual(updated_material.quantity, 120)

    def test_negative_quantity(self):
        """Test that a ValidationError is raised for a negative quantity."""
        with self.assertRaises(ValidationError):
            material = Material(
                hardware_name='Hardware Store A',
                category_name='Building materials',
                material_name='Cement',
                brand_name='BrandX',
                description='High-quality cement',
                price=50.00,
                quantity=-10
            )
            material.full_clean()  # Triggers validation

    def test_exceeding_description_length(self):
        """Test that a ValidationError is raised if description length exceeds 100 characters."""
        with self.assertRaises(ValidationError):
            material = Material(
                hardware_name='Hardware Store A',
                category_name='Building materials',
                material_name='Cement',
                brand_name='BrandX',
                description='A' * 101,  # Exceeds the max length of 100 characters
                price=50.00,
                quantity=100
            )
            material.full_clean()  # Triggers validation

    def test_invalid_image_extension(self):
        """Test that a ValidationError is raised for unsupported image formats."""
        with self.assertRaises(ValidationError):
            material = Material(
                hardware_name='Hardware Store A',
                category_name='Building materials',
                material_name='Cement',
                brand_name='BrandX',
                description='High-quality cement',
                price=50.00,
                quantity=100,
                image='file.txt'  # Unsupported extension
            )
            material.full_clean()  # Triggers validation
