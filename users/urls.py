from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users import views

router = DefaultRouter()
router.register("Addresses", views.AddressView, basename="Addresses")

urlpatterns = [
    path("signup/", views.UserSignupView.as_view()),
    # path('login/',views.UserLoginView.as_view()),
    path("", include(router.urls)),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
