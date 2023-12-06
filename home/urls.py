from django.urls import include, path
from rest_framework.routers import DefaultRouter

from home import views

router = DefaultRouter()
router.register("stores", views.StoreView, basename="stores")
router.register("products", views.ProductView, basename="products")
router.register("wishlist", views.WishlistView, basename="wishlist")
router.register("reviews", views.ReviewView, basename="reviews")

urlpatterns = [
    path("", include(router.urls)),
]
