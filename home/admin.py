from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from home import models

# Register your models here.


class StoreCategoryAdmin(TranslationAdmin):
    list_display = ("name", "name_ar", "image")
    list_filter = ("name",)


class StoreAdmin(TranslationAdmin):
    list_display = ("name", "name_ar", "image", "category")
    list_filter = ("name", "category")


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "image")
    list_filter = ("name",)


class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "image")
    list_filter = ("name",)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "image",
        "category",
        "brand",
        "inventory",
    )
    list_filter = ("id", "name", "category", "brand", "store", "inventory")


class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user",)
    list_filter = (
        "user",
        "product",
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user",)
    list_filter = (
        "user",
        "product",
    )


admin.site.register(models.StoreCategory, StoreCategoryAdmin)
admin.site.register(models.Store, StoreAdmin)
admin.site.register(models.ProductCategory, ProductCategoryAdmin)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Wishlist, WishlistAdmin)
admin.site.register(models.Review, ReviewAdmin)
