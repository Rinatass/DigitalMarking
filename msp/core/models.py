from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f'{self.name} ({self.owner.username})'


class MarkingCode(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='codes')
    batch = models.ForeignKey('ProductBatch', on_delete=models.CASCADE, related_name='codes', null=True, blank=True)
    code = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

class MovementLog(models.Model):
    code = models.ForeignKey(MarkingCode, on_delete=models.CASCADE, related_name='movements')
    location = models.CharField(max_length=255)
    moved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.code.code} moved to {self.location} at {self.timestamp}'

class ProductBatch(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='batches')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Партия {self.name} ({self.product.name}) на {self.quantity} шт.'
