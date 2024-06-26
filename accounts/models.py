from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50)
    sugar=models.IntegerField()
    coffee=models.IntegerField()
    flour=models.IntegerField()
    chocolate=models.IntegerField()