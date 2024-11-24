from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/')
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', default='product_images/default.jpg', blank=True, null=True)
    old_price = models.FloatField()
    new_price = models.FloatField()
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product_id', 'user_id')
