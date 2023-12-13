from django.utils.translation import gettext
from rest_framework import serializers

from cart import models
from cart.conf import PAYMENT_STATUS_PENDING
from cart.helpers import CurrentAddressDefault, CurrentCartDefault
from home.serializers import SimpleProductSerializer


class CartSerializer(serializers.ModelSerializer):
    total = serializers.IntegerField(default=0)

    class Meta:
        model = models.Cart
        fields = ("id", "total")


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
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pending_status = serializers.HiddenField(default=PAYMENT_STATUS_PENDING)
    user_address = serializers.HiddenField(default=CurrentAddressDefault())
    total = serializers.HiddenField(default=0)

    class Meta:
        model = models.Order
        fields = "__all__"

    def validate(self, attrs):
        if not models.CartItem.objects.filter(
            cart=self.context["request"].user.cart
        ).exists():
            raise serializers.ValidationError(gettext("cart_empty"))
        return super().validate(attrs)
