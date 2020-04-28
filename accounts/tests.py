from django.test import TestCase
from django.contrib.auth.models import User
from .models import Supplier
from django.core.files.uploadedfile import SimpleUploadedFile
from go2people.utils import random_string_generator


def create_supplier(**kwargs):
    user_dict = {
        'username': random_string_generator(10),
        'password': random_string_generator(20),
    }

    if 'username' in kwargs:
        user_dict['username'] = kwargs.get('username')
    if 'password' in kwargs:
        user_dict['password'] = kwargs.get('password')

    user = User.objects.create(**user_dict)

    supplier_dict = {
        'user': user,
        'thumbnail': SimpleUploadedFile(name='supplier_image_test.jpg', content=open(
            'media/profile_images/tests/supplier_image_test.jpg', 'rb').read(), content_type='image/jpeg')
    }

    return Supplier.objects.create(**supplier_dict)


class SupplierModelTest(TestCase):

    def test_creation_supplier(self):
        username = "delta"
        supplier = create_supplier(username=username)
        self.assertTrue(isinstance(supplier, Supplier))
        self.assertEqual(supplier.__str__(), username)
