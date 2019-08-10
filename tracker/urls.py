from django.urls import path

from . import views

urlpatterns = [
    path(r"", views.home, name="home"),
    path(r"events", views.events, name="events"),
]
