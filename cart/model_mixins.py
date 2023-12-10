from django_lifecycle import BEFORE_CREATE, hook
from rest_framework import serializers


class CartItemMixin:
    @hook(BEFORE_CREATE)
    def on_creation(self):
        from cart.models import CartItem

        instance = CartItem.objects.filter(product=self.product, cart=self.cart).first()
        if instance is not None:
            raise serializers.ValidationError("product already exists")
