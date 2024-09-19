from django.db import models

# Create your models here.

from django.db import models
from material.models import Material
from datetime import datetime
from homeowner.models import Homeowner
from supplier.models import Supplier
from django.db.models import JSONField

# Create your models here.

class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    material=models.ForeignKey(Material, on_delete=models.CASCADE, related_name="order")
    order_date=models.DateTimeField(default=datetime.now)
    status=models.CharField(max_length=200)
    cart_data = JSONField()
    homeowner = models.ForeignKey(Homeowner, on_delete=models.CASCADE, related_name='order')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='order')
    
    
    def __str__(self):
        return f"{self.order_date} {self.status}"