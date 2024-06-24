from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView
urlpatterns=[
    path('',LoginView.as_view(template_name='login.html'),name='login'),
    path('login/',login,name='login'),
    path("register/",register,name="register")

]