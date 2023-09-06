from django.urls import include, path
from rest_framework.routers import DefaultRouter

from home import views

router = DefaultRouter()
router.register("products", views.ProductView, basename="products")
router.register("wishlist", views.WishlistView, basename="wishlist")
router.register("Reviews", views.ReviewView, basename="Reviews")

urlpatterns = [
    path("stores/", views.StoreView.as_view()),
    path("", include(router.urls)),
]
