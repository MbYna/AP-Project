from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Product, ProductIngredient


class Register(UserCreationForm):
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "category", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "نام کالا"}),
            "price": forms.NumberInput(attrs={"placeholder": "قیمت کالا"}),
        }
