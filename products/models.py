'''
This module contains models represented by two classes:
- Categroy: a class used to represent a Category
- Product: a class used to represent a Product
'''
from datetime import datetime

from django.db import models
from django.db.models.signals import pre_save

from accounts.models import Supplier
from go2people.utils import unique_slug_generator


SLUG_HELP_TEXT = "The slug must be unique, \
it will be generated automatically if the field is blank."


class Category(models.Model):
    '''
    A class used to represent a Category
    '''
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, help_text=SLUG_HELP_TEXT)
    description = models.TextField(blank=True)

    class Meta:
        '''
        This is a Meta class
        '''
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    '''
    A class used to represent a Product
    '''
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, help_text=SLUG_HELP_TEXT)
    categories = models.ManyToManyField(Category)
    description = models.TextField()
    image = models.ImageField(upload_to='products')

    PR = 'PR'
    VMBO = 'VMBO'
    MBO = 'MBO'
    HBO = 'HBO'
    OP = 'OP'
    SCHOOL_TYPE_CHOICES = [
        (PR, 'praktijkonderwijs'),
        (VMBO, 'vmbo'),
        (MBO, 'mbo'),
        (HBO, 'hbo'),
        (OP, 'opleidingsbedrijf')
    ]
    school_type = models.CharField(
        max_length=48,
        choices=SCHOOL_TYPE_CHOICES
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField('Date published', default=datetime.now)
    end_at = models.DateTimeField('Publishing end date')

    def __str__(self):
        return self.name

    def is_product_available(self):
        ''' Check if the product is available, so it can be published
        '''
        now = datetime.now()
        return self.created_at <= now <= self.end_at
    is_product_available.boolean = True


def slug_generator(sender, instance, *args, **kwargs):
    ''' Generate a unique slug for a given object
    '''
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Product)
pre_save.connect(slug_generator, sender=Category)
