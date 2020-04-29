'''
This module contains models represented by:
- Supplier: a class used to represent a Supplier
'''
from django.db import models
from django.contrib.auth.models import User


class Supplier(models.Model):
    '''
    A class used to represent a Supplier
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='profile_images')

    def __str__(self):
        return self.user.username
