from django.test import TestCase


from payments.models import Payment
from django.db.utils import IntegrityError

class PaymentModelUnhappyPathTests(TestCase):

    def test_payment_without_amount(self):
        
        with self.assertRaises(IntegrityError):
            Payment.objects.create(
                checkout_request_id='test_request_id',
                phone_number='254700123456',
                status='Pending',
                transaction_id='test_transaction_id'
            )

      

    def test_duplicate_checkout_request_id(self):
    
        Payment.objects.create(
            checkout_request_id='test_request_id',
            amount=100.50,
            phone_number='254700123456',
            status='Pending',
            transaction_id='test_transaction_id'
        )

        with self.assertRaises(IntegrityError):
            Payment.objects.create(
                checkout_request_id='test_request_id',  
                amount=200.75,
                phone_number='254700654321',
                status='Completed',
                transaction_id='another_transaction_id'
            )

      

    


