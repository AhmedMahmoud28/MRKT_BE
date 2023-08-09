from django.contrib import admin
from cart import models
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date") 
    list_filter = ("date",)  

class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity") 
    list_filter = ("id",)  

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "pending_status", "owner") 
    list_filter = ("owner", "pending_status")  
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity") 
    list_filter = ("order",)  
        
admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.CartItem, CartItemAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
