from django.db import transaction
from rest_framework import serializers

from home import models
from users.serializers import SimpleUserSerializer


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


class ProductSerializer(serializers.ModelSerializer):
    is_fav = serializers.SerializerMethodField(method_name="fav")
    rate = serializers.SerializerMethodField(method_name="rate_avg")
    brand_name = serializers.CharField(default=None)

    class Meta:
        model = models.Product
        fields = ["name", "image", "price", "brand_name", "is_fav", "rate"]

    def fav(self, obj):
        Q = self.context["query_set1"]
        return obj.id in Q

    def rate_avg(self, obj):
        Q = self.context["query_set2"]
        if obj.id in Q.keys():
            return Q.get(obj.id)
        else:
            return 0


class ProductDetailsSerializer(serializers.ModelSerializer):
    is_fav = serializers.SerializerMethodField(method_name="fav")
    rate = serializers.SerializerMethodField(method_name="rate_avg")
    comment = serializers.SerializerMethodField(method_name="comments")

    class Meta:
        model = models.Product
        fields = ["name", "image", "price", "brand", "is_fav", "rate", "comment"]

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent["brand"] = instance.brand.name
        return represent

    def fav(self, obj):
        Q = self.context["query_set1"]
        return obj.id in Q

    def rate_avg(self, obj):
        Q = self.context["query_set2"]
        if obj.id in Q.keys():
            return Q.get(obj.id)
        else:
            return 0

    def comments(self, obj):
        Query = models.Review.objects.select_related("user").filter(product=obj)
        return Reviewserializer(Query, many=True).data
