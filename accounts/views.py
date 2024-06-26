from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from APProject import urls


def loginPage(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.info(request,'نام کاربری یا رمز عبور اشتباه است')
            
    return render(request, "accounts/login.html")

def registerPage(request):
    form=Register()
    if request.method=="POST":
        form=Register(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'حساب شما با موفقیت ساخته شد')
            return redirect('login')
    context={'form':form}
    return render(request, "accounts/register.html",context)

