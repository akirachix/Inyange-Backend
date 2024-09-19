from django.db import models
# from user.models import User


# Create your models here.

class Homeowner(models.Model):
    homeowner_id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(User, related_name='homeowners', on_delete=models.CASCADE)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.homeowner_id} {self.address}"