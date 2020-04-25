from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        categories = self.cleaned_data.get('categories')
        if categories and categories.count() > 6:
            raise ValidationError('Maximum six categories are allowed.')

        return self.cleaned_data
