from django.urls import path, include
from users import views, serializers
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('userlist',views.Userlist, basename='userlist')


urlpatterns = [
    path('signup/',views.UserSignup.as_view()),
    path('login/',views.UserLogin.as_view()),
    # path('',include(router.urls))
]
