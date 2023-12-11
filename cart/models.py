import uuid

from django.db import models
from django_lifecycle import LifecycleModel

from cart.conf import PAYMENT_STATUS_CHOICES, PAYMENT_STATUS_PENDING
from cart.model_mixins import CartItemMixin
from home.models import Product
from users.models import Address, User

# Create your models here.


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} {self.user.name}"


class CartItem(LifecycleModel, CartItemMixin):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cartitems"
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cart} {self.product} {self.quantity}"


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    user_address = models.ForeignKey(Address, on_delete=models.PROTECT)
    pending_status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING
    )
    total = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.owner, self.pending_status


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product.name
