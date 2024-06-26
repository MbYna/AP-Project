
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage , name="login"),
    path('register/', views.registerPage , name="register"),
    path('menu/',views.menuPage ,name="menu")
]
