from django.db import models

# Create your models here.

class Material(models.Model):
    material_id = models.AutoField(primary_key= True)
    CATEGORY_CHOICES = [
        ('Building materials', 'Building materials'),
        ('Finishing materials', 'Finishing materials'),
        ('Hardware and tools', 'Hardware and tools'),
    ]
    category_name = models.CharField(max_length= 50, choices = CATEGORY_CHOICES)
    material_name = models.CharField(max_length= 50)
    brand_name = models.CharField(max_length= 200)
    description = models.CharField(max_length= 100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f"{self.material_name} {self.description}"