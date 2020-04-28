from django.test import TestCase
from django.contrib.auth.models import User
from .models import Supplier
from django.core.files.uploadedfile import SimpleUploadedFile


def create_supplier(username):
    password = "JAwqpyuW3M7dqScr"
    thumbnail = SimpleUploadedFile(name='supplier_image_test.jpg', content=open(
        'media/profile_images/tests/supplier_image_test.jpg', 'rb').read(), content_type='image/jpeg')
    user = User.objects.create(username=username, password=password)

    return Supplier.objects.create(user=user, thumbnail=thumbnail)


class SupplierModelTest(TestCase):

    def test_creation_supplier(self):
        supplier = create_supplier("user01")
        self.assertTrue(isinstance(supplier, Supplier))
        self.assertEqual(supplier.__str__(), supplier.user.username)
