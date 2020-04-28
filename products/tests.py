from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product, Category
from django.contrib.auth.models import User
from accounts.tests import create_supplier
from django.urls import reverse
from go2people.utils import random_string_generator


def create_category(name):
    return Category.objects.create(name=name)


class CategoryModelTest(TestCase):

    def test_creation_category(self):
        """
        __str__() should return the same category name of creation
        """
        category = create_category("workshops")
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(category.__str__(), category.name)


def create_product(**kwargs):
    categories = [
        create_category("paint"),
        create_category("tools")
    ]

    product_dict = {
        'supplier': create_supplier(),
        'name': 'Painting classes',
        'description': random_string_generator(size=250),
        'image': SimpleUploadedFile(name='product_image_test.jpg', content=open(
            'media/products/tests/product_image_test.jpg', 'rb').read(), content_type='image/jpeg'),
        'school_type': ('PR', 'praktijkonderwijs'),
        'price': 99.99,
        'created_at': datetime.now(),
        'end_at': datetime.now() + timedelta(days=10)
    }

    for key, value in kwargs.items():
        if key != 'categories':
            product_dict[key] = value
        else:
            categories = value

    product = Product.objects.create(**product_dict)
    product.categories.set(categories)

    return product


class ProductModelTest(TestCase):

    def test_creation_product(self):
        """
        __str__() should return the same product name of creation
        """
        name = "product name"
        product = create_product(name=name)
        self.assertTrue(isinstance(product, Product))
        self.assertEqual(product.__str__(), name)

    def test_product_is_available(self):
        """
        is_product_available() should return True for products whose end_at is in the future.
        """
        created_at = datetime.now()
        end_at = datetime.now() + timedelta(days=1)
        product = create_product(created_at=created_at, end_at=end_at)
        self.assertIs(product.is_product_available(), True)

    def test_product_is_not_available(self):
        """
        is_product_available() should return False for products whose end_at is before created_at.
        """
        created_at = datetime.now()
        end_at = datetime.now() - timedelta(days=1)
        product = create_product(created_at=created_at, end_at=end_at)
        self.assertIs(product.is_product_available(), False)

    def test_product_created_in_future_is_not_available(self):
        """
        is_product_available() should return False for products whose created_at in the future.
        """
        created_at = datetime.now() + timedelta(days=1)
        end_at = datetime.now() + timedelta(days=10)
        product = create_product(created_at=created_at, end_at=end_at)
        self.assertIs(product.is_product_available(), False)
