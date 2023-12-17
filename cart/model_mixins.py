from django_lifecycle import AFTER_CREATE, BEFORE_CREATE, hook
from rest_framework import serializers


class CartItemMixin:
    @hook(BEFORE_CREATE)
    def on_creation(self):
        from cart.models import CartItem
        from home.models import Product

        instance = CartItem.objects.filter(product=self.product, cart=self.cart).first()
        if instance is not None:
            raise serializers.ValidationError("product already exists")

        inventory_product = Product.objects.get(id=self.product.id).inventory
        if not inventory_product >= self.quantity:
            raise serializers.ValidationError("Not_enough_stock")


class OrderMixin:
    @hook(BEFORE_CREATE)
    def creating_order(self):
        from cart.models import Cart, CartItem

        self.total = (
            Cart.objects.filter(user=self.owner)
            .annotate_total()
            .values("total")
            .first()["total"]
        )

        cartitems = list(
            CartItem.objects.all()
            .select_related("product")
            .filter(cart=self.owner.cart)
        )
        for item in cartitems:
            if not item.product.inventory >= item.quantity:
                raise serializers.ValidationError(
                    item.product.name + " has_no_enough_stock"
                )

    @hook(AFTER_CREATE)
    def after_creating_order(self):
        from django.db.models import F

        from cart.models import Cart, CartItem, OrderItem
        from home.models import Product

        cart = Cart.objects.filter(user=self.owner).first()
        cartitems = CartItem.objects.filter(cart=cart)
        orderitems = [
            OrderItem(
                order=self,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.price,
            )
            for item in cartitems
        ]
        OrderItem.objects.bulk_create(orderitems)
        for item in orderitems:
            Product.objects.filter(id=item.product.id).update(
                inventory=F("inventory") - item.quantity
            )
        CartItem.objects.filter(cart=cart).delete()
