from django.db import models
# from user.models import User

# Create your models here.


class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key= True)
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    company_name = models.CharField(max_length= 200)
    location = models.CharField(max_length= 200)

    


    def __str__(self):
        return f"{self.company_name} {self.location}"