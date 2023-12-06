from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from home.managers import ProductManager
from users.models import User

# Create your models here.


class StoreCategory(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to="images/storecategory-images", null=True, blank=True
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Store Categories"


class Store(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/store-images", null=True, blank=True)
    category = models.ForeignKey(StoreCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class ProductCategory(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to="images/productcategory-images", null=True, blank=True
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Product Categories"


class Brand(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/brand-images", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/product-images", null=True, blank=True)
    price = models.PositiveIntegerField(default=0)
    inventory = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    store = models.ManyToManyField(Store)

    objects = ProductManager()

    @property
    def final_price(self):
        return self.price * 100

    def __str__(self):
        return f"{self.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.product_id}"  # type: ignore

    class Meta:
        unique_together = (
            "user",
            "product",
        )


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()

    def __str__(self):
        return f"{self.user} {self.product_id}"  # type: ignore

    class Meta:
        unique_together = (
            "user",
            "product",
        )
