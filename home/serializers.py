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
    product = SimpleProductSerializer(many=False)

    class Meta:
        model = models.Wishlist
        fields = ["id", "product"]


class AddtoWishlistserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wishlist
        fields = ["product"]

    def save(self, **kwargs):
        with transaction.atomic():
            user_id = self.context["user_id"]
            product_added = self.validated_data["product"]  # type: ignore
            self.instance = (
                models.Wishlist.objects.select_related("product").filter(user_id=user_id, product__id=product_added.id).first()
            )
            if self.instance is None:
                return models.Wishlist.objects.select_related("product").create(user_id=user_id, product=product_added)
            elif self.instance is not None:
                return self.instance.delete()


class Reviewserializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = models.Review
        fields = ["user", "product", "rate", "comment"]


class AddReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ["product", "rate", "comment"]

    def save(self, **kwargs):
        with transaction.atomic():
            user_id = self.context["user_id"]
            product_added = self.validated_data["product"]  # type: ignore
            rate_added = self.validated_data["rate"]  # type: ignore
            comment_added = self.validated_data["comment"]  # type: ignore
            self.instance = (
                models.Review.objects.select_related("product").filter(user_id=user_id, product__id=product_added.id).first()
            )
            if self.instance is None:
                return models.Review.objects.select_related("product").create(
                    user_id=user_id,
                    product=product_added,
                    rate=rate_added,
                    comment=comment_added,
                )
            elif self.instance is not None:
                self.instance.rate = rate_added
                self.instance.comment = comment_added
                self.instance.save()
                return self.instance


class ProductSerializer(serializers.ModelSerializer):
    is_fav = serializers.SerializerMethodField(method_name="fav")
    rate = serializers.SerializerMethodField(method_name="rate_avg")

    class Meta:
        model = models.Product
        fields = ["name", "image", "price", "brand", "is_fav", "rate"]

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
