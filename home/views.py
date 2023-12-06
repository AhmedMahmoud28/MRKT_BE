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
    queryset = models.Product.objects.select_related("brand").all()
    filterset_fields = ["category", "brand", "store"]
    search_fields = ["^name"]
    ordering_fields = ["name", "price"]
    ordering = ["id"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.ProductDetailsSerializer
        else:
            return serializers.ProductSerializer

    def get_serializer_context(self):
        return {
            "query_set1": models.Wishlist.objects.filter(
                user=self.request.user
            ).values_list("product", flat=True),
            "query_set2": {
                item["product"]: item["avg"]
                for item in (
                    models.Review.objects.select_related("product")
                    .values("product")
                    .annotate(avg=Avg("rate"))
                )
            },
        }


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

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.AddReviewSerializer
        return serializers.Reviewserializer

    def get_queryset(self):
        user = self.request.user
        return models.Review.objects.select_related("user", "product").filter(user=user)
