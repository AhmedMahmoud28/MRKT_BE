from rest_framework import serializers

from home import models


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ["id", "name", "price"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = ["name", "image"]


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = ["name", "image"]


class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Wishlist
        fields = "__all__"


class WishlistDetailedSerializer(WishlistSerializer):
    product = SimpleProductSerializer()


class Reviewserializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Review
        fields = "__all__"


class ReviewDetailedSerializer(Reviewserializer):
    product = SimpleProductSerializer()


class ReviewDataSerializer(serializers.ModelSerializer):
    product = serializers.HiddenField(default="")

    class Meta:
        model = models.Review
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    is_fav = serializers.BooleanField(default=False)  # type: ignore
    avg_rate = serializers.FloatField(default=0)
    brand_name = serializers.CharField(default=None)

    class Meta:
        model = models.Product
        fields = ["name", "image", "price", "brand_name", "is_fav", "avg_rate"]


class ProductDetailsSerializer(ProductSerializer):
    reviews = ReviewDataSerializer(many=True, read_only=True, source="review")

    class Meta:
        model = models.Product
        fields = [
            "name",
            "image",
            "price",
            "brand_name",
            "is_fav",
            "avg_rate",
            "reviews",
        ]
