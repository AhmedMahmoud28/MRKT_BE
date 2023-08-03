from django.urls import path, include
from cart import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register("",views.CartViewSet)

cart_router = routers.NestedDefaultRouter(router, "", lookup="cart")
cart_router.register("items",views.CartItemViewSet, basename='cart-items')


urlpatterns = [
    path('',include(router.urls)),
    path('',include(cart_router.urls)),
]