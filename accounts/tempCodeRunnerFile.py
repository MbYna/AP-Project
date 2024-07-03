def menuPage(request):
    products = Product.objects.all()
    for product in products:
        print(product.name)
