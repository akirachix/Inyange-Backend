# user/models.py
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

USER_ROLES = [
    ('admin', 'Admin'),
    ('homeowner', 'Homeowner'),
    ('supplier', 'Supplier'),
]

class User(AbstractUser, PermissionsMixin):
    phone_number = models.CharField(max_length=18)
    user_role = models.CharField(max_length=20, choices=USER_ROLES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'user_role']

    def __str__(self):
        return self.email
