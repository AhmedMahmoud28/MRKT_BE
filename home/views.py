from django.db.models import Avg
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from home import models, serializers


class StoreView(GenericViewSet, ListModelMixin):
    filterset_fields = ["category"]
    serializer_class = serializers.StoreSerializer
    queryset = models.Store.objects.all()


class ProductView(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
):
    queryset = models.Product.objects.all().annotate_brand().annotate_rate()
    serializer_class = serializers.ProductSerializer
    permission_classes = ()
    filterset_fields = ["category", "brand", "store"]
    search_fields = ["^name"]
    ordering_fields = ["name", "price"]
    ordering = ["id"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.ProductDetailsSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.annotate_is_wishlisted(self.request)
        return super().get_queryset()


class WishlistView(ModelViewSet):
    serializer_class = serializers.WishlistSerializer
    queryset = models.Wishlist.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.WishlistDetailedSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.select_related("product").filter(user=user)
        return super().get_queryset()


class ReviewView(ModelViewSet):
    serializer_class = serializers.Reviewserializer
    queryset = models.Review.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.ReviewDetailedSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return models.Review.objects.select_related("user", "product").filter(
                user=user
            )
        return super().get_queryset()
