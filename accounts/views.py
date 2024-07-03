from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ProductForm, Register
from django import forms
from .models import Product, Cart, CartItem, Storage, Category, ProductIngredient
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "نام کاربری یا رمز عبور اشتباه است")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def signup_view(request):
    form = Register()
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "حساب شما با موفقیت ساخته شد")
            return redirect("login")
    context = {"form": form}
    return render(request, "accounts/register.html", context)


def menu_view(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "accounts/menu.html", context)


def admin_view(request):
    return render(request, "accounts/admin.html")


def create_product_view(request):
    ProductIngredientFormset = forms.inlineformset_factory(
        Product,
        ProductIngredient,
        fields=["ingredient", "amount"],
        extra=Storage.objects.count(),
    )

    if request.method == "POST":
        form = ProductForm(request.POST)
        formset_data = ProductIngredientFormset(
            request.POST,
            initial=[
                {"ingredient": ingredient} for ingredient in Storage.objects.all()
            ],
        )
        if form.is_valid() and formset_data.is_valid():
            with transaction.atomic():
                product = form.save()
                formset_data.instance = product
                formset_data.save()

            return redirect("myadmin")

    form = ProductForm()
    formset = ProductIngredientFormset(
        initial=[{"ingredient": ingredient} for ingredient in Storage.objects.all()]
    )
    context = {"form": form, "formset": formset}
    return render(request, "accounts/addproduct.html", context)


def storage_view(request):
    if request.method == "POST":
        # Get user input
        ingredient_name = request.POST.get("name")
        ingredient_amount = request.POST.get("amount")
        ingredient_unit = request.POST.get("unit")

        # Create an storage instance and save it to the database
        Storage.objects.create(
            name=ingredient_name, amount=ingredient_amount, unit=ingredient_unit
        )

        # redirect to the previous page
        return redirect(request.headers.get("Referer", "/"))

    return render(request, "accounts/storage.html", {"storages": Storage.objects.all()})


def cart_view(request):
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_purchased=False)

    context = {"cart": cart}
    return render(request, "accounts/cart.html", context)

@login_required
@require_POST
def add_to_cart_view(request, product_pk):
    user = request.user
    product = get_object_or_404(Product, pk=product_pk)
    quantity = int(request.POST.get('quantity', 1))
    if product.has_sufficient_ingredients(quantity):
        cart, _ = Cart.objects.get_or_create(user=user, is_purchased=False)
        cart.add_to_cart(product, quantity)
        return redirect("cart")
    else:
        available = product.max_quantity_to_sell()
        messages.warning(request, f'مواد اولیه مورد نیاز موجود نیست. فقط میتوانید {available} واحد اضافه کنید.')
        return redirect("menu")

def update_cart_view(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user, is_purchased=False)

    for cart_item in cart.cart_items.all():
        quantity = request.POST.get(f'quantity_{cart_item.product.pk}')
        if int(quantity) > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart')

def checkout_view(request):
    user = request.user
    cart = Cart.objects.get(user=user, is_purchased=False)
    for cart_item in cart.cart_items.all():
        for product_ingredient in cart_item.ingredients_set.all():
            product_ingredient.storage.amount -= product_ingredient.amount * quantity
            product_ingredient.storage.save()
    cart.is_purchased = True

    cart.save()
    return redirect("home")

@login_required
def cart_history_view(request):
    user = request.user
    carts = Cart.objects.filter(user=user, is_purchased=True)
    context = {"carts": carts}
    return render(request, "accounts/cart_history.html", context)
