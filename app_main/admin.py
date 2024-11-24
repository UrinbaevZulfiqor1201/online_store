from django.contrib import admin
from .models import Product, Category, Cart


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'old_price', 'new_price')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    list_filter = ('title',)
    search_fields = ('title', 'description')


admin.site.register(Cart)