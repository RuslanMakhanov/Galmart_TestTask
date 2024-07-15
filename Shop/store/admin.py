from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Shop, Order

# Регистрация модели Shop
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'open']  

# Регистрация модели Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['status', 'amount', 'shop']
    list_filter = ['status', 'shop']
    search_fields = ['shop__name']