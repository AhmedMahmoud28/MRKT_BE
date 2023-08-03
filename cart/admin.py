from django.contrib import admin
from cart import models
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "date") 
    list_filter = ("date",)  

class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity") 
    list_filter = ("id",)  

admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.CartItem, CartItemAdmin)
