from django.db import models
from django.db.models import Max, Min


class CustomQuerySet(models.QuerySet):
    def min(self):
        return self.aggregate(Min("price")).get("price__min")

    def max(self):
        return self.aggregate(Max("price")).get("price__max")

    def annotate_brand(self):
        from django.db.models import F

        return self.annotate(brand_name=F("brand__name"))


class ProductManager(models.Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)

    def min_price(self):
        return self.get_queryset().min()

    def max_price(self):
        return self.get_queryset().max()
