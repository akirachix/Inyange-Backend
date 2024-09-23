from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Payment
from django.db import IntegrityError

User = get_user_model()

class PaymentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password',
            email='testuser@example.com'
        )

    def test_create_payment(self):
        """Test creating a Payment instance with all required fields."""
        payment = Payment.objects.create(
            
            checkout_request_id='unique_request_id',
            amount=100.00,
            phone_number='254717244476',
            status='Pending'
        )
        self.assertIsNotNone(payment.id) 

    def test_payment_without_user(self):
       
            Payment.objects.create(
                checkout_request_id='unique_request_id',
                amount=100.00,
                phone_number='254717244476',
                status='Pending'
                
                
            )
            
        
    def test_payment_without_amount(self):
        """Test creating a payment without an amount raises an error."""
        with self.assertRaises(IntegrityError):
            Payment.objects.create(
                
                checkout_request_id='unique_request_id',
                phone_number='254717244476',
                status='Pending'
        )


    def test_payment_with_invalid_phone_number(self):
        """Test creating a payment with an invalid phone number."""
        payment = Payment.objects.create(
            checkout_request_id='unique_request_id',
            amount=100.00,
            phone_number='invalid_phone',
            status='Pending'
        )
        self.assertEqual(payment.phone_number, 'invalid_phone')

    def test_payment_status_choices(self):
        """Test that the status field accepts valid values."""
        valid_statuses = ['Pending', 'Completed', 'Failed']
        for status in valid_statuses:
            payment = Payment.objects.create(
                checkout_request_id='unique_request_id',
                amount=100.00,
                phone_number='254717244476',
                status=status
            )
            self.assertEqual(payment.status, status)
            
    def test_str_method(self):
        """Test the __str__ method of the Payment model."""
        payment = Payment.objects.create(
            checkout_request_id='unique_request_id',
            amount=100.00,
            phone_number='254717244476',
            status='Pending'
            )
        expected_str = "Payment unique_request_id - Pending by 100.00"
        self.assertEqual(str(payment), expected_str)


