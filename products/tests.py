from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product, Category
from django.contrib.auth.models import User
from accounts.tests import create_supplier
from django.urls import reverse


def create_category(name):
    return Category.objects.create(name=name)


class CategoryModelTest(TestCase):

    def test_creation_category(self):
        category = create_category("workshops")
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(category.__str__(), category.name)


def create_product(name):
    supplier = create_supplier("delta")
    categories = [
        create_category("paint"),
        create_category("tools")
    ]
    description = "This is a description"
    image = SimpleUploadedFile(name='product_image_test.jpg', content=open(
        'media/products/tests/product_image_test.jpg', 'rb').read(), content_type='image/jpeg')
    school_type = ('PR', 'praktijkonderwijs')
    price = 99.99
    created_at = datetime.now()
    end_at = datetime.now() + timedelta(days=1)

    product = Product.objects.create(
        supplier=supplier,
        name=name,
        description=description,
        image=image,
        school_type=school_type,
        price=price,
        created_at=created_at,
        end_at=end_at
    )

    product.categories.set(categories)

    return product


class ProductModelTest(TestCase):

    def test_creation_product(self):
        product = create_product("Painting classes")
        self.assertTrue(isinstance(product, Product))
        self.assertEqual(product.__str__(), product.name)
