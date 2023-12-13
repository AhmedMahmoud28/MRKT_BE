from django.db import models
from django.db.models import F, OuterRef, Subquery, Sum


class CartQuerySet(models.QuerySet):
    def annotate_total(self):
        from cart.models import CartItem

        return self.annotate(
            total=Subquery(
                CartItem.objects.filter(cart_id=OuterRef("id"))
                .select_related("product")
                .values("cart_id")
                .annotate(total=Sum(F("product__price") * F("quantity")))
                .values("total")
            )
        )
