
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage , name="login"),
    path('register/', views.registerPage , name="register"),
    path('logout/', views.logoutPage, name="logout"),
    path('menu/',views.menuPage ,name="menu"),
    path('myadmin/',views.adminPage, name="myadmin"),
    path('addproduct/',views.addProduct, name="add"),
    path('storage/',views.storagePage, name="storage"),
    path('cart/', views.cart , name="cart"),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('edit_ingredient/', views.edit_ingredient, name='edit_ingredient'),
]
