'''
This module contains tests represented by:
- TestModels: a class to test models
- TestUrls: a class to test urls
- TestViews: a class to test views
'''
from datetime import datetime, timedelta
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.core.files.uploadedfile import SimpleUploadedFile


from products.models import Product, Category
from products.views import index_view, product_view
from accounts.tests import create_supplier
from go2people.utils import random_string_generator


def create_category(name):
    ''' Create a category with the given name
    '''
    return Category.objects.create(name=name)


def create_product(**kwargs):
    ''' Create a product with the given arguments
    '''
    categories = [
        create_category("paint"),
        create_category("tools")
    ]

    product_dict = {
        'supplier': create_supplier(),
        'name': 'Painting classes',
        'description': random_string_generator(size=250),
        'image': SimpleUploadedFile(
            name='product_image_test.jpg',
            content=open('media/products/tests/product_image_test.jpg',
                         'rb').read(), content_type='image/jpeg'),
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


class TestModels(TestCase):
    '''
    A class to test models
    '''
    def test_creation_category(self):
        """
        __str__() should return the same category name of creation
        """
        name = "Category name"
        category = create_category(name)
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(category.__str__(), name)

    def test_category_is_assigned_slug(self):
        """
        category.slug should return the same slug = "category-slug"
        """
        category = create_category("Category Slug")
        slug = "category-slug"
        self.assertEqual(category.slug, slug)

    def test_creation_product(self):
        """
        __str__() should return the same product name of creation
        """
        name = "Product name"
        product = create_product(name=name)
        self.assertTrue(isinstance(product, Product))
        self.assertEqual(product.__str__(), name)

    def test_product_is_assigned_slug(self):
        """
        product.slug should return the same slug = "product-slug"
        """
        product = create_product(name="Product Slug")
        slug = "product-slug"
        self.assertEqual(product.slug, slug)

    def test_product_is_available(self):
        """
        is_product_available() should return True for
        products whose end_at is in the future.
        """
        created_at = datetime.now()
        end_at = datetime.now() + timedelta(days=1)
        product = create_product(created_at=created_at, end_at=end_at)
        self.assertIs(product.is_product_available(), True)

    def test_product_is_not_available(self):
        """
        is_product_available() should return False for
        products whose end_at is before created_at.
        """
        created_at = datetime.now()
        end_at = datetime.now() - timedelta(days=1)
        product = create_product(created_at=created_at, end_at=end_at)
        self.assertIs(product.is_product_available(), False)

    def test_product_created_in_future_is_not_available(self):
        """
        is_product_available() should return False for
        products whose created_at is in the future.
        """
        created_at = datetime.now() + timedelta(days=1)
        end_at = datetime.now() + timedelta(days=10)
        product = create_product(created_at=created_at, end_at=end_at)
        self.assertIs(product.is_product_available(), False)


class TestUrls(TestCase):
    '''
    A class to test urls
    '''
    def test_index_url_resolves(self):
        """
        resolve(url).func should return index_view.
        """
        url = reverse('index')
        self.assertEqual(resolve(url).func, index_view)

    def test_product_url_resolves(self):
        """
        resolve(url).func should return product_view.
        """
        url = reverse('product', args=['product-slug'])
        self.assertEqual(resolve(url).func, product_view)


class TestViews(TestCase):
    '''
    A class to test views
    '''
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.product_url = reverse('product', args=['product-01'])
        create_product(name='Product 01')

    def test_index_view(self):
        """
        response.status_code should return 200.
        """
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/index.html')

    def test_product_view(self):
        """
        response.status_code should return 200.
        """
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product.html')

    def test_product_view_404_error(self):
        """
        response.status_code should return 404 (page not found).
        """
        response = self.client.get(reverse('product', args=['product-20']))
        self.assertEqual(response.status_code, 404)
