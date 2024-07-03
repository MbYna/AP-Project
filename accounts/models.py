from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


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
        max_quantity = float("inf")  # Initialize with positive infinity
        for ingredient in self.ingredients.all():
            storage_amount = Storage.objects.get(name=ingredient.name).amount
            ingredient_quantity_needed = ingredient.amount
            max_quantity = min(
                max_quantity, storage_amount // ingredient_quantity_needed
            )
        return max_quantity

    def __str__(self):
        return self.name


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

    @property
    def price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name
