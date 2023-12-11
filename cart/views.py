from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from cart import models, serializers


class CartViewSet(GenericViewSet, ListModelMixin):
    queryset = models.Cart.objects.select_related("user")
    serializer_class = serializers.CartSerializer
    pagination_class = None

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CartItemViewSet(ModelViewSet):
    serializer_class = serializers.CartItemSerializer
    queryset = models.CartItem.objects.select_related("cart", "product")
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(cart=user.cart)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "update":
            return serializers.UpdateCartItemSerializer
        return super().get_serializer_class()


class OrderViewSet(ModelViewSet):
    queryset = models.Order.objects.prefetch_related("items", "items__product")
    serializer_class = serializers.OrderSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateOrderSerializer(
            data=request.data,
            context={
                "user_id": self.request.user.id,  # type: ignore
                "cart_id": self.request.user.cart.id,  # type: ignore
            },
        )  # type: ignore
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.CreateOrderSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        if user.is_authenticated:
            return self.queryset.filter(owner=user)
        return super().get_queryset()
