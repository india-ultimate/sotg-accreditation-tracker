import json

from django.core.cache import cache
from django.shortcuts import render

from uc_api_helpers import get_registrations, get_tournaments
from .forms import AccreditationForm

CACHE_TIMEOUT = 60 * 60  # 1 hour


def index(request):
    return render(request, "tracker/index.html")


def events(request):
    data = json.loads(_events_data())
    context = {"events": data}
    return render(request, "tracker/event-list.html", context)


def event_page(request, event_id):
    events = json.loads(_events_data())
    event = [event for event in events if event["id"] == event_id][0]
    registrations = json.loads(_registrations_data(event_id))
    context = {"registrations": registrations, "event": event}
    return render(request, "tracker/event-page.html", context)


def accreditation_form(request, event_id, team_name):
    registrations = json.loads(_registrations_data(event_id))

    team_emails = set()
    forms = []
    for registration in registrations:
        team = registration["Team"]
        if team is None or team["name"] != team_name:
            continue

        person = registration["Person"]
        if person["email_address"] in team_emails:
            continue

        team_emails.add(person["email_address"])
        forms.append(
            AccreditationForm(
                initial={
                    "name": person["full_name"],
                    "email": person["email_address"],
                    "uc_username": person["slug"],
                }
            )
        )

    context = {"forms": forms, "team_name": team_name}
    return render(request, "tracker/accreditation-form.html", context)


def _events_data():
    """Get event data either from the cache or from Ultimate Central"""

    key = "event-list"
    data = cache.get(key)
    if not data:
        data = json.dumps(get_tournaments())
        cache.set(key, data, CACHE_TIMEOUT)

    return data


def _registrations_data(event_id):
    """Get registration data for an event (cached or fresh from Ultimate Central)"""

    key = "event-registrations-{}".format(event_id)
    data = cache.get(key)
    if not data:
        data = json.dumps(get_registrations(event_id))
        cache.set(key, data, CACHE_TIMEOUT)

    return data
