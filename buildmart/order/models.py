from django.db import models
from django.db import models
from material.models import Material
from datetime import datetime
from django.utils import timezone
from django.db.models import JSONField


# Create your models here.

class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    material=models.ForeignKey(Material, on_delete=models.CASCADE, related_name="order")
    order_date=models.DateTimeField(default=timezone.now)
    status=models.CharField(max_length=200)
    cart_data = JSONField()
    
    
    def __str__(self):
        return f"{self.order_date} {self.status}"