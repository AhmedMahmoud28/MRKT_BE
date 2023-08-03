from django.contrib import admin
from home import models
# Register your models here.

class StoreCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "image") 
    list_filter = ("name",)  
    

class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "category") 
    list_filter = ("name","category")  
    
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "image") 
    list_filter = ("name",)  
    
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "image") 
    list_filter = ("name",)  
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "category", "brand") 
    list_filter = ("id", "name", "category", "brand", "store")  

admin.site.register(models.StoreCategory, StoreCategoryAdmin)
admin.site.register(models.Store, StoreAdmin)
admin.site.register(models.ProductCategory, ProductCategoryAdmin)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Product, ProductAdmin)