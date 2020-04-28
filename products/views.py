from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Product
from datetime import datetime


def indexView(request):
    # products = Product.objects.all()
    now = datetime.now()
    products = Product.objects.filter(end_at__gt=now, created_at__lt=now)
    context = {
        'page_title': 'List products',
        'title': 'List products',
        'currency': '€',
        'categories': 'Categories',
        'school_type': 'School Type',
        'published_at': 'Published at',
        'end_at': 'End at',
        'products': products,
    }
    return render(request, 'products/index.html', context)


def productView(request, product_slug):
    query = Product.objects.filter(slug=product_slug)
    # product = get_object_or_404(Product, pk=product_id)
    product = get_object_or_404(query)
    context = {
        'page_title': product.name,
        'title': 'Product Details',
        'currency': '€',
        'categories': 'Categories',
        'school_type': 'School Type',
        'published_at': 'Published at',
        'end_at': 'End at',
        'product': product,
    }

    return render(request, 'products/product.html', context)
