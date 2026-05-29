from django.urls import path

from . import views


app_name = "jokes"

urlpatterns = [
    path("", views.home, name="home"),
]
