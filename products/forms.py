from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Product


class CategoryForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        slug = self.cleaned_data.get('slug')

        error_list = []
        error_exist = False

        if slug:
            qs = self._meta.model._default_manager.filter(**{'slug': slug})
            initial_value = self.initial.get('slug')
            qs = qs.exclude(**{'slug': initial_value})
            if qs.exists():
                error_slug = 'A Category with this slug already exists.'
                error_exist = True
                error_list.append(error_slug)

        if error_exist:
            raise ValidationError(error_list)


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        slug = self.cleaned_data.get('slug')
        categories = self.cleaned_data.get('categories')
        price = self.cleaned_data.get('price')
        created_at = self.cleaned_data.get('created_at')
        end_at = self.cleaned_data.get('end_at')

        error_list = []
        error_exist = False

        if slug:
            qs = self._meta.model._default_manager.filter(**{'slug': slug})
            initial_value = self.initial.get('slug')
            qs = qs.exclude(**{'slug': initial_value})
            if qs.exists():
                error_slug = 'A product with this slug already exists.'
                error_exist = True
                error_list.append(error_slug)

        if categories and categories.count() > 6:
            error_categories = 'One to six categories are allowed.'
            error_exist = True
            error_list.append(error_categories)

        if price and price < 0:
            error_price = 'Price must be more than 0.'
            error_exist = True
            error_list.append(error_price)

        if created_at and end_at and created_at >= end_at:
            error_exist = True
            error_date = 'Publishing end date must be after Creation date.'
            error_list.append(error_date)

        if error_exist:
            raise ValidationError(error_list)

        return self.cleaned_data
