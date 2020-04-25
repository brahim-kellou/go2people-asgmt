from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Product


def index(request):
    products = Product.objects.all()
    context = {
        'title': 'List products',
        'products': products
    }
    return render(request, 'products/index.html', context)
