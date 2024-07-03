from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from collections import OrderedDict
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.db.models import Sum

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to="product/", blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        blank=True,
        null=True,
    )
    ingredients = models.ManyToManyField("Storage", through="ProductIngredient")

    def has_sufficient_ingredients(self, n):
        for ingredient in self.product_ingredients.all():
            storage = Storage.objects.get(name=ingredient.ingredient.name)
            if storage.amount < n * ingredient.amount:
                return False
        return True

    def max_quantity_to_sell(self):
        quantities = [
            Storage.objects.get(name=ingredient.ingredient.name).amount // ingredient.amount
            for ingredient in self.product_ingredients.all()
            if ingredient.amount > 0
        ]
        return min(quantities) if quantities else 0
        
    def __str__(self):
        return self.name

    @classmethod
    def get_best_selling_products(cls, top_n=10):
        return (
            cls.objects.annotate(total_sales=Sum("cart_items__quantity"))
            .order_by("-total_sales")[:top_n]
        )


class ProductIngredient(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_ingredients"
    )
    ingredient = models.ForeignKey(
        "Storage", on_delete=models.CASCADE, related_name="product_ingredients"
    )
    amount = models.FloatField(default=0)

    def __str__(self):
        return self.product.name + " - " + self.ingredient.name


class Storage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    amount = models.FloatField(default=0)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Cart(models.Model):
    class CartTypes(models.TextChoices):
        delivery = "DELIVERY", "Delivery"
        dine_in = "DINE_IN", "Dine-in"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    is_purchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    purchased = models.DateTimeField(default=timezone.now)
    order_type = models.CharField(
        max_length=10, choices=CartTypes.choices, default=CartTypes.delivery
    )

    @property
    def total_price(self):
        return sum(cart_item.price for cart_item in self.cart_items.all())

    def add_to_cart(self, product, quantity=1):
        if not product.has_sufficient_ingredients(quantity):
            return False

        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)
        cart_item.quantity += quantity
        cart_item.save()
        return True

    def remove_from_cart(self, product):
        cart_item = CartItem.objects.filter(cart=self, product=product).first()
        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

    def __str__(self):
        return self.product.name


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_sale_in_dayframe(cls, product, dayframe):
        sales = (
            cls.objects.filter(
                product=product,
                cart__purchased__gte=timezone.now() - timedelta(days=dayframe),
            )
            .values("cart__purchased__date")
            .annotate(total_sales=Sum("quantity"))
            .order_by("-cart__purchased__date")
            .values("cart__purchased__date", "total_sales")
        )

        sales_dict = OrderedDict([
            (sale["cart__purchased__date"].isoformat(), sale["total_sales"])
            for sale in sales
        ])
        
        for i in range(dayframe):
            date = (timezone.now() - timedelta(days=i)).date().isoformat()
            if date not in sales_dict:
                sales_dict[date] = 0

        return OrderedDict(reversed(list(sales_dict.items())))

    @property
    def price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name

