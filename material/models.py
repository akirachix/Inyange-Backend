import os
from django.db import models
from django.core.exceptions import ValidationError

def validate_image_format(image):
    if image:
        ext = os.path.splitext(image.name)[1].lower()
        valid_extensions = ['.jpg', '.jpeg', '.png']
        if ext not in valid_extensions:
            raise ValidationError(f'Unsupported file extension: {ext}. Allowed extensions are: .jpg, .jpeg, .png.')

class Material(models.Model):
    material_id = models.AutoField(primary_key=True)
    hardware_name = models.CharField(max_length=200) 
    CATEGORY_CHOICES = [
        ('Building materials', 'Building materials'),
        ('Finishing materials', 'Finishing materials'),
        ('Hardware and tools', 'Hardware and tools'),
    ]
    category_name = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    material_name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=200)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='materials_images/', validators=[validate_image_format]) 

    def __str__(self):
        return f"{self.material_name} {self.description}"  
