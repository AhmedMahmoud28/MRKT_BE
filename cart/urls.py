from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from cart import views

router = DefaultRouter()
router.register("carts", views.CartViewSet, basename="carts")
router.register("orders", views.OrderViewSet, basename="orders")


cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", views.CartItemViewSet, basename="cart-items")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(cart_router.urls)),
]
