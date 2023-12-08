from django.db import models
from django.db.models import Avg, Exists, F, Max, Min, OuterRef


class CustomQuerySet(models.QuerySet):
    def min(self):
        return self.aggregate(Min("price")).get("price__min")

    def max(self):
        return self.aggregate(Max("price")).get("price__max")

    def annotate_brand(self):
        return self.annotate(brand_name=F("brand__name"))

    def annotate_is_wishlisted(self, request):
        from home.models import Wishlist

        return self.annotate(
            is_fav=Exists(
                Wishlist.objects.filter(user=request.user, product=OuterRef("id"))
            )
        )

    def annotate_rate(self):
        return self.annotate(avg_rate=Avg("review__rate"))


class ProductManager(models.Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)

    def min_price(self):
        return self.get_queryset().min()

    def max_price(self):
        return self.get_queryset().max()
