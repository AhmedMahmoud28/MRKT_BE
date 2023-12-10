from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext
from rest_framework import serializers

from cart import models
from cart.helpers import CurrentCartDefault
from home.serializers import SimpleProductSerializer
from users.models import Address
from users.serializers import AddressSerializer


class CartSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = models.Cart
        fields = ("id", "total")

    def get_total(self, cart: models.Cart):
        items = cart.items.select_related("product")
        return sum(item.quantity * item.product.price for item in items)


class CartItemSerializer(serializers.ModelSerializer):
    cart = serializers.HiddenField(default=CurrentCartDefault())
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = models.CartItem
        fields = "__all__"

    def get_sub_total(self, obj):
        return obj.quantity * obj.product.price


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ["quantity"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = models.OrderItem
        fields = ["id", "product", "quantity", "unit_price", "sub_total"]

    def total(self, obj):
        return obj.quantity * obj.unit_price


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_address = AddressSerializer()

    class Meta:
        model = models.Order
        fields = [
            "id",
            "date",
            "pending_status",
            "owner",
            "items",
            "total",
            "user_address",
        ]


class CreateOrderSerializer(serializers.Serializer):
    def create(self, validated_data):
        with transaction.atomic():
            cart_id = self.context["cart_id"]
            user_id = self.context["user_id"]
            address = get_object_or_404(Address, user_id=user_id, address_status=True)

            if not models.Cart.objects.filter(pk=cart_id).exists():
                raise serializers.ValidationError("this is invalid cart id")

            elif (
                cart_id
                != models.Cart.objects.filter(user_id=user_id).values_list(
                    "id", flat=True
                )[0]
            ):
                raise serializers.ValidationError(
                    "you don't have permission for this action"
                )

            elif not models.CartItem.objects.filter(cart_id=cart_id).exists():
                raise serializers.ValidationError(gettext("cart_empty"))

            cartitems = models.CartItem.objects.filter(cart_id=cart_id)
            total = sum(item.product.price * item.quantity for item in cartitems)
            order = models.Order.objects.create(
                owner_id=user_id, total=total, user_address=address
            )
            orderitems = [
                models.OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.product.price,
                )
                for item in cartitems
            ]
            models.OrderItem.objects.bulk_create(orderitems)
            for item in orderitems:
                Q = models.Product.objects.values_list("id", flat=True)
                for i in Q:
                    if item.product.id == i:  # type: ignore
                        models.Product.objects.filter(id=i).update(
                            inventory=F("inventory") - item.quantity
                        )
            models.CartItem.objects.filter(cart_id=cart_id).delete()
            return order
