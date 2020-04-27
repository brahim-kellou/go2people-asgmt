from django.test import TestCase
from django.utils import timezone
from .models import Product, Category


class ProductModelTest(TestCase):

    def create_product(self, name="Product", description="This is a description"):
        return Product.objects.create(name=name, description=name, created_at=timezone.now())

    def test_product_creation(self):
        product = self.create_product()
        self.assertTrue(isinstance(product, Product))
        self.assertEqual(product.__unicode__(), product.name)
