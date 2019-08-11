from django.urls import path

from . import views

urlpatterns = [
    path(r"", views.home, name="home"),
    path(r"events", views.events, name="events"),
    path(r"event/<int:event_id>", views.event_page, name="event_page"),
]
