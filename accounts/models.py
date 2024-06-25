from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(User):
    name=models.CharField(max_length=500)
    phone=models.IntegerField()
