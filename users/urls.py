from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from users import views

router = DefaultRouter()
router.register("addresses", views.AddressView, basename="addresses")
router.register("signup", views.UserSignupView, basename="signup")

urlpatterns = [
    # path('login/',views.UserLoginView.as_view()),
    path("", include(router.urls)),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
]
