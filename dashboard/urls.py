from django.urls import path

from dashboard import views

urlpatterns = [
    path("", views.Boardview.as_view()),
]
