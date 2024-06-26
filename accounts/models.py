from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def has_sufficient_ingredients(self, n):
        for ingredient in self.ingredients.all():
            if ingredient.amount * n > Storage.objects.get(name=ingredient.name).amount:
                return False
        return True
                
    def max_quantity_to_sell(self):
        max_quantity = float('inf')  # Initialize with positive infinity
        for ingredient in self.ingredients.all():
            storage_amount = Storage.objects.get(name=ingredient.name).amount
            ingredient_quantity_needed = ingredient.amount
            max_quantity = min(max_quantity, storage_amount // ingredient_quantity_needed)
        return max_quantity

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    amount = models.FloatField(default=0)
    product=models.ManyToManyField(Product)
    

class Storage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    amount = models.FloatField(default=0)

