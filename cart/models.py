from django.db import models
import uuid
from home.models import Product
from users.models import User
# Create your models here.


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4 ,editable=False, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} {self.user.name}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cartitems")
    quantity = models.PositiveIntegerField(default=1)
        
    def __str__(self):
        return f"{self.cart} {self.product} {self.quantity}"  
    
        
class Order(models.Model):
    
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    date = models.DateTimeField(auto_now_add=True)
    pending_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.pending_status


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name = "items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.product.name