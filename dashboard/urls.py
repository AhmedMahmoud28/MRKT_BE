from django.urls import include, path

from dashboard import views

urlpatterns = [
    path('',views.Boardview.as_view()),
]