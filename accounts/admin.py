# admin.py

from django.contrib import admin
from .models import Product, Storage, Category

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Storage)
