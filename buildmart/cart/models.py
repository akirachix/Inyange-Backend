from django.db import models 
from django.contrib.auth import get_user_model 

User = get_user_model() 

class UserCart(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart') 
    cart = models.JSONField(default=dict) 