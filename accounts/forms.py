from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Customer
from django import forms

class Register(UserCreationForm):
    class Meta:
        model=Customer
        fields=['name','username','email','password','phone']
