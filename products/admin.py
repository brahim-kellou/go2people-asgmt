'''
This module contains admin configurations
'''
from django.contrib import admin
from .models import Product, Category
from .forms import ProductForm


class ProductAdmin(admin.ModelAdmin):
    '''
    A class to configurate products in the admin side
    '''
    form = ProductForm


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
