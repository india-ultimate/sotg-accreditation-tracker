import json

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse

from tracker.models import Accreditation
from uc_api_helpers import get_registrations, get_tournaments
from .forms import accreditationformset_factory

CACHE_TIMEOUT = 60 * 60  # 1 hour


def index(request):
    return render(request, "tracker/index.html")


def events(request):
    data = json.loads(_events_data())
    context = {"events": data}
    return render(request, "tracker/event-list.html", context)


@login_required
def event_page(request, event_id):
    events = json.loads(_events_data())
    event = [event for event in events if event["id"] == event_id][0]
    registrations = json.loads(_registrations_data(event_id))
    context = {"registrations": registrations, "event": event}
    return render(request, "tracker/event-page.html", context)


@login_required
def accreditation_form(request, event_id, team_name):
    registrations = json.loads(_registrations_data(event_id))

    def extract_info(person):
        return (
            ("name", person["full_name"]),
            ("uc_username", person["slug"]),
            ("email", person["email_address"]),
        )

    team_players = sorted(
        {
            extract_info(registration["Person"])
            for registration in registrations
            if (
                registration["Team"] is not None
                and registration["Team"]["name"] == team_name
            )
        }
    )

    player_data = [dict(player) for player in team_players]
    emails = [player["email"] for player in player_data]
    existing_players = Accreditation.objects.filter(email__in=emails)
    existing_emails = {player.email for player in existing_players}
    new_players = [
        player
        for player in player_data
        if player["email"] not in existing_emails
    ]
    if request.method == "POST":
        AccreditationFormSet = accreditationformset_factory(extra=0)
        formset = AccreditationFormSet(request.POST)
        if formset.is_valid():
            formset.save()
    else:
        AccreditationFormSet = accreditationformset_factory(len(new_players))
        # Use a filtered queryset of players in the current team
        formset = AccreditationFormSet(
            queryset=existing_players, initial=new_players
        )
    context = {"formset": formset, "team_name": team_name}
    return render(request, "tracker/accreditation-form.html", context)


def logout_view(request):
    logout(request)
    return redirect(reverse("events"))


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
