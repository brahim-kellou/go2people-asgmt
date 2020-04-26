from django.db import models
from datetime import datetime
from accounts.models import Supplier


class Category(models.Model):
    name = models.CharField(unique=True, max_length=200)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products')
    description = models.TextField()

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
