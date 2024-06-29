from django.shortcuts import render,redirect
from django.http import HttpResponse
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

def logoutPage(request):
    logout(request)
    return redirect('home')

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

def menuPage(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request,'accounts/menu.html',context)

def adminPage(request):
    return render(request,'accounts/admin.html')

def addProduct(request):
    form=ProductForm()
    if request.method=="POST":
        form=ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myadmin')
    context={'form':form}
    return render(request, "accounts/addproduct.html",context)


def storagePage(request):
    if request.method == 'POST':
        # Get user input
        ingredient_name = request.POST.get('ingr')
        ingredient_amount = request.POST.get('left')

        # Create an Ingredient instance and save it to the database
        Storages.objects.create(name=ingredient_name, amount=ingredient_amount)

        # Optionally, you can return an HTTP response or redirect to another page
        return HttpResponse("Data added successfully!")
    return render(request,'accounts/storage.html')


def cart(request):
    order_cart = Orders.objects.filter(user=request.user).first
    total = 0
    items = []
    if order_cart:
        for item in Orders_Product.objects.filter(Orders=order_cart):
            all = item.product.price * item.quantity
            items.append({
                'product': item.product,
                'quantity': item.quantity,
                'price': item.product.price,
                'item_total': all,
                'id': item.id
            })
            total += all
    return render(request, 'accounts/cart.html', {'items': items ,'total': total})

def add_to_cart(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if product.has_sufficient_ingredients(quantity):   #آیا می‌توان محصول را با تعداد مشخص شده خریداری کرد یا خیر
        order, created_ = Orders.objects.get_or_create(user=request.user)
        order_product, created_ = Orders_Product.objects.get_or_create(order=order, product=product)
        if not created_:
            order_product.quantity += quantity
        else:
            order_product.quantity = quantity
        order_product.save()

        for Ingredient in product.Ingredient_set.all(): #مقدار موجودی محصول در انبار کاهش می‌یابد
            Ingredient.Storage.amount -= Ingredient.amount * quantity
            Ingredient.Storage.save()

        messages.success(request, "محصول با موفقیت به سبد خرید اضافه شد")
    else:
        #available = product.max_quantity_to_sell()میتونیم بگیم که چند واحد اضافه کنه تا بتونه محصول رو دریافت کنه
        messages.warning(request, "مواد اولیه برای ساخت محصول کافی نیست")
    return redirect('cart')






