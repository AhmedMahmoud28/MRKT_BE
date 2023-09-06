from datetime import datetime

from django.db.models import Avg, Count, Max, Min, Sum
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Order, OrderItem
from home.models import Product
from users.models import User


class Boardview(APIView):
    def get(self, request):
        users = User.objects.count()
        reg_users = User.objects.filter(
            date__gte=datetime(2023, 8, 21, 13, 22),
            date__lte=datetime(2023, 8, 21, 13, 24),
        ).count()
        orders = Order.objects.count()
        Order_in_two_mins = Order.objects.filter(
            date__gte=datetime(2023, 8, 21, 13, 8),
            date__lte=datetime(2023, 8, 21, 13, 10),
        ).count()
        Ordertotal_in_two_mins = (
            Order.objects.filter(
                date__gte=datetime(2023, 8, 21, 13, 8),
                date__lte=datetime(2023, 8, 21, 13, 10),
            )
            .aggregate(Sum("total"))
            .get("total__sum")
        )
        avg_orders = Order.objects.all().aggregate(Avg("total")).get("total__avg")
        min_order = Order.objects.aggregate(Min("total")).get("total__min")
        max_order = Order.objects.aggregate(Max("total")).get("total__max")
        products = Product.objects.count()

        min_product = Product.objects.aggregate(Min("price")).get("price__min")
        min_product1 = Product.objects.min_price()  # type: ignore

        max_product = Product.objects.aggregate(Max("price")).get("price__max")
        max_product1 = Product.objects.max_price()  # type: ignore

        list_of_orders = Order.objects.annotate(items_count=Count("items")).values("id", "items_count").order_by("-items_count")
        list_of_products = (
            OrderItem.objects.annotate(Quantity=Sum("quantity")).values("product__name", "Quantity").order_by("-Quantity")
        )

        return Response(
            {
                "Total_Users": users,
                "Total_Users_Registered": reg_users,
                "Total_Orders": orders,
                "Orders_in_2_mins": Order_in_two_mins,
                "Ordertotal_in_2_mins": Ordertotal_in_two_mins,
                "Avg_Total_Of_Orders": avg_orders,
                "Min_Total_for_Order": min_order,
                "Max_Total_for_Order": max_order,
                "Total_Products": products,
                "Min_Price_for_Product": min_product,
                "Min1_Price_for_Product": min_product1,
                "Max_Price_for_Product": max_product,
                "Max1_Price_for_Product": max_product1,
                "Orders_List": list_of_orders,
                "Products_List": list_of_products,
            }
        )
