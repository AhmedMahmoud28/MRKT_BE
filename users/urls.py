from django.urls import path, include
from users import views, serializers
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# router = DefaultRouter()
# router.register('userlist',views.Userlist, basename='userlist')


urlpatterns = [
    path('signup/',views.UserSignup.as_view()),
    path('login/',views.UserLogin.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('',include(router.urls))
]
