from django.urls import path, include
from home import views, serializers
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('wishlist',views.WishlistView, basename='wishlist')


urlpatterns = [
    path('stores/',views.storeview.as_view()),
    path('products/',views.productview.as_view()),
    path('',include(router.urls))
]