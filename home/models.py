from django.db import models
# Create your models here.

class StoreCategory(models.Model): 
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/storecategory-images")
    
    def __str__(self):
        return f"{self.name}"
        
    class Meta:
        verbose_name_plural = "Store Categories"

class Store(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/store-images")
    category = models.ForeignKey(StoreCategory, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name}"
        
class ProductCategory(models.Model): 
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/productcategory-images")
    
    def __str__(self):
        return f"{self.name}"    
    
    class Meta:
        verbose_name_plural = "Product Categories"

class Brand(models.Model): 
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/brand-images")
    
    def __str__(self):
        return f"{self.name}"

class Product(models.Model): 
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/product-images")
    price = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    store = models.ManyToManyField(Store)
    
    def __str__(self):
        return f"{self.name}"    
    