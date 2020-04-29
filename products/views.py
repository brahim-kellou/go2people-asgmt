'''
This module contains views:
- index_view: Returns the view of product list (index).
- product_view: Returns the view of product details (product).
'''
from datetime import datetime
from django.shortcuts import get_object_or_404, render

from products.models import Product


def index_view(request):
    '''
    Returns the view of product list (index)
    '''
    now = datetime.now()
    products = Product.objects.filter(end_at__gt=now, created_at__lt=now)
    context = {
        'page_title': 'List products',
        'title': 'List products',
        'currency': '€',
        'categories': 'Categories',
        'school_type': 'School Type',
        'published_at': 'Date published',
        'end_at': 'Publishing end date',
        'products': products,
    }
    return render(request, 'products/index.html', context)


def product_view(request, product_slug):
    '''
    Returns the view of product details (product)
    '''
    query = Product.objects.filter(slug=product_slug)
    product = get_object_or_404(query)
    context = {
        'page_title': product.name,
        'title': 'Product Details',
        'currency': '€',
        'categories': 'Categories',
        'school_type': 'School Type',
        'published_at': 'Date published',
        'end_at': 'Publishing end date',
        'product': product,
    }

    return render(request, 'products/product.html', context)
