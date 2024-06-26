from django.shortcuts import render,redirect,get_object_or_404
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
    for product in products:
        print(product.name) 
    context={'products':products}
    return render(request,'accounts/menu.html')

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
    return render(request,'accounts/storage.html')

def cart(request, product_id):
    # Retrieve the product based on the product ID
    product = get_object_or_404(Product, id=product_id)
    n = int(request.POST.get('quantity', 1))
    if product.has_sufficient_ingredients(n):
        order, created = Orders.objects.get_or_create(user=request.user)
        order_product, created_ = OrderProduct.objects.get_or_create(order=order, product=product)
        if not created_:
            order_product.quantity = n
        else:
            order_product.quantity += n
        order_product.save()
        for product_ingredient in product.productingredient_set.all():
            product_ingredient.storage.amount -= product_ingredient.amount * quantity
            product_ingredient.storage.save()
    cart = Cart.objects.get(user=request.user)

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}  # Set the default quantity to 1
    )

    # If the product was already in the cart, increment the quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Redirect to the cart page
    return redirect('cart_view')  # Replace 'cart_view' with your actual cart view name
