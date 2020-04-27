from django.db import models
from datetime import datetime
from accounts.models import Supplier
from go2people.utils import unique_slug_generator
from django.db.models.signals import pre_save


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(
        unique=True, blank=True, help_text="The slug must be unique, it will be generated automatically if the field is blank.")
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
    created_at = models.DateTimeField(default=datetime.now)
    end_at = models.DateTimeField()

    def __str__(self):
        return self.name


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Product)
pre_save.connect(slug_generator, sender=Category)
