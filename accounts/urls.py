from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.signup_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home, name="home"),
    path("menu/", views.menu_view, name="menu"),
    path("myadmin/", views.admin_view, name="myadmin"),
    path("addproduct/", views.create_product_view, name="add"),
    path("product/", views.create_product_view, name="add"),
    path("storage/", views.storage_view, name="storage"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/history", views.cart_history_view, name="cart_history"),
    path("cart/purchase", views.checkout_view, name="checkout"),
    path("cart/<int:product_pk>", views.add_to_cart_view, name="add_to_cart"),
    path('update-cart/', views.update_cart_view, name='update_cart'),
]
