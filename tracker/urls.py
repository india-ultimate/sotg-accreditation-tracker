from django.urls import path

from . import views

urlpatterns = [
    path(r"", views.index, name="index"),
    path(r"events", views.events, name="events"),
    path(r"event/<int:event_id>", views.event_page, name="event_page"),
    path(r"event/<int:event_id>/<team_name>", views.accreditation_form, name="accreditation_form"),
]
