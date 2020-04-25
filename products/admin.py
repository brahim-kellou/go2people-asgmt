from django.contrib import admin
from .models import Product, Category
from .forms import ProductForm


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
