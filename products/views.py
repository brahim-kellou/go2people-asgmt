from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Product


def indexView(request):
    products = Product.objects.all()
    context = {
        'title': 'List products',
        'products': products
    }
    return render(request, 'products/index.html', context)


def productView(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'title': 'Product Details',
        'product': product
    }

    return render(request, 'products/product.html', context)
