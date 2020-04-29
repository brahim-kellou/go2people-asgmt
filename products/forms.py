'''
This module contains forms:
- CategoryForm: A class represent the form of creating a category
- ProductForm: A class represent the form of creating a product
'''
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Product


CATEGORY_ERROR_SLUG = 'A category with this slug already exists.'

PRODUCT_ERROR_SLUG = 'A product with this slug already exists.'
PRODUCT_ERROR_CATEGORIES = 'One to six categories are allowed.'
PRODUCT_ERROR_PRICE = 'Price must be more than zero (price > 0).'
PRODUCT_ERROR_END_AT = 'Publishing end date cannot be before the date of creation.'

class CategoryForm(ModelForm):
    '''
    A class represent the form of creating a category
    '''
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        ''' A mothod to check the form before saving
        '''
        slug = self.cleaned_data.get('slug')

        error_list = []

        if slug:
            initial_value = self.initial.get('slug')
            qs = self.Meta.model.objects.filter(slug=slug)
            qs = qs.exclude(slug=initial_value)
            if qs.exists():
                error_list.append({'slug': PRODUCT_ERROR_SLUG})

        if error_list:
            raise ValidationError(error_list)


class ProductForm(ModelForm):
    '''
    A class represent the form of creating a product
    '''
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        ''' A mothod to check the form before saving
        '''
        slug = self.cleaned_data.get('slug')
        categories = self.cleaned_data.get('categories')
        price = self.cleaned_data.get('price')
        created_at = self.cleaned_data.get('created_at')
        end_at = self.cleaned_data.get('end_at')

        error_list = []

        # check if the slug already exists
        if slug:
            initial_value = self.initial.get('slug')
            qs = self.Meta.model.objects.filter(slug=slug)
            qs = qs.exclude(slug=initial_value)
            if qs.exists():
                error_list.append({'slug': PRODUCT_ERROR_SLUG})

        # check if the product has one to six categories
        if categories and not 1 <= categories.count() <= 6:
            error_list.append({'categories': PRODUCT_ERROR_CATEGORIES})

        # check if the price is less than 0
        if price and price < 0:
            error_list.append({'price': PRODUCT_ERROR_PRICE})

        # check if end_at is after created_at
        if created_at and end_at and created_at >= end_at:
            error_list.append({'end_at': PRODUCT_ERROR_END_AT})

        if error_list:
            raise ValidationError(error_list)

        return self.cleaned_data
