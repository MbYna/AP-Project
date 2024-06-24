from django.shortcuts import render


# Create your views here.
def login(request):
    if request.method=='GET':
        context={}
        render(request,'login.html',context)
def register(request):
    pass


    