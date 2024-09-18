from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserManagerTest(TestCase):
    def setUp(self):
        self.email = "user@example.com"
        self.username = "testuser"
        self.first_name = "Test"
        self.last_name = "User"
        self.phone_number = "1234567890"
        self.password = "password123"
        self.user_role = "supplier"
        

    def test_create_user_success(self):
        user = User.objects.create_user(
            email=self.email,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            phone_number=self.phone_number,
            user_role=self.user_role,
            password=self.password,
        )
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
        self.assertEqual(user.phone_number, self.phone_number)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(
                email="",  
                username=self.username,
                first_name=self.first_name,
                last_name=self.last_name,
                phone_number=self.phone_number,
                user_role=self.user_role,
                password=self.password,
            )
        self.assertEqual(str(context.exception), "The Email field must be set")

    def test_create_superuser_success(self):
        superuser = User.objects.create_superuser(
            email=self.email,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            phone_number=self.phone_number,
            user_role=self.user_role,
            password=self.password
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_without_email(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_superuser(
                email="",  
                username=self.username,
                first_name=self.first_name,
                last_name=self.last_name,
                phone_number=self.phone_number,
                user_role=self.user_role,
                password=self.password,
            )
        self.assertEqual(str(context.exception), "The Email field must be set")

class UserModelTest(TestCase):
    def setUp(self):
        self.email = "user@example.com"
        self.username = "testuser"
        self.first_name = "Test"
        self.last_name = "User"
        self.phone_number = "1234567890"
        self.password = "password123"

    def test_user_role_homeowner(self):
        user = User.objects.create_user(
            email=self.email,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            phone_number=self.phone_number,
            user_role="homeowner",
            password=self.password
        )
        self.assertEqual(user.user_role, "homeowner")
        self.assertFalse(user.is_superuser)

    def test_user_role_supplier(self):
        user = User.objects.create_user(
            email=self.email,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            phone_number=self.phone_number,
            user_role="supplier",
            password=self.password
        )
        self.assertEqual(user.user_role, "supplier")
        self.assertFalse(user.is_superuser)

    def test_user_string_representation(self):
        user = User.objects.create_user(
            email=self.email,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            phone_number=self.phone_number,
            user_role="supplier",  
            password=self.password
        )
        self.assertEqual(str(user), user.email)  # String representation is the email

    
    
