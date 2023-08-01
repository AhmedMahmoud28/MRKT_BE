from django.db import models
import uuid
from home.models import Product
# Create your models here.

class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4 ,editable=False, primary_key=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"
  
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cartitems")
    quantity = models.PositiveIntegerField(default=1)
        
    def __str__(self):
        return f"{self.cart} {self.product} {self.quantity}"  
    