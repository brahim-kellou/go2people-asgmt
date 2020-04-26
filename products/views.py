from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Product
from datetime import datetime


def indexView(request):
    # products = Product.objects.all()
    now = datetime.now()
    products = Product.objects.filter(end_at__gt=now, created_at__lt=now)
    context = {
        'title': 'List products',
        'currency': '€',
        'categories': 'Categories',
        'school_type': 'School Type',
        'published_at': 'Published at',
        'end_at': 'End at',
        'products': products,
    }
    return render(request, 'products/index.html', context)


def productView(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'title': 'Product Details',
        'currency': '€',
        'categories': 'Categories',
        'school_type': 'School Type',
        'published_at': 'Published at',
        'end_at': 'End at',
        'product': product,
    }

    return render(request, 'products/product.html', context)
