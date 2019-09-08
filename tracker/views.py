import datetime
import json

import arrow
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse

from tracker.models import Accreditation
from uc_api_helpers import get_registrations, get_tournaments
from .forms import accreditationformset_factory, AccreditationFormSetHelper

CACHE_TIMEOUT = 60 * 60  # 1 hour


def index(request):
    return render(request, "tracker/index.html")


def events(request):
    data = json.loads(_events_data())
    context = {"events": data}
    return render(request, "tracker/event-list.html", context)


def admin_teams(registrations, email):
    my_admin_teams = {
        registration["Team"]["name"]
        for registration in registrations
        if (
            registration["Person"]["email_address"] == email
            and registration["role"] in {"admin", "captain"}
        )
    }
    return my_admin_teams


def get_valid_accreditations(emails):
    valid_after_date = arrow.now().shift(months=-18).date()
    return Accreditation.objects.filter(
        email__in=emails, date__gte=valid_after_date
    )


def group_registrations_by_team(registrations, accreditations):
    registrations_by_team = dict()
    # {
    #     "ATC": {
    #         "Alex": {
    #             "roles": ["player", "admin"],
    #             "email": "foo@bar.com",
    #             "accreditation": "Advanced",
    #         },
    #         "Mai": {...},
    #     }
    # }
    for registration in registrations:
        if registration["Team"] is None:
            team_name = "No team"
        else:
            team_name = registration["Team"]["name"]
        person_name = registration["Person"]["full_name"]
        email = registration["Person"]["email_address"]

        team = registrations_by_team.setdefault(team_name, {})
        player = team.setdefault(person_name, {})
        roles = player.setdefault("roles", [])

        roles.append(registration["role"])
        player["email"] = registration["Person"]["email_address"]
        if email in accreditations:
            player["accreditation"] = accreditations[email].type

    return registrations_by_team


@login_required
def event_page(request, event_id):
    events = json.loads(_events_data())
    event = [event for event in events if event["id"] == event_id][0]
    registrations = json.loads(_registrations_data(event_id))
    emails = [r["Person"]["email_address"] for r in registrations]
    accreditations = {A.email: A for A in get_valid_accreditations(emails)}

    context = {
        "registrations": registrations,
        "event": event,
        "admin_teams": admin_teams(registrations, request.user.email),
        "registrations_by_team": group_registrations_by_team(
            registrations, accreditations
        ),
    }
    return render(request, "tracker/event-page.html", context)


@login_required
def accreditation_form(request, event_id, team_name):
    registrations = json.loads(_registrations_data(event_id))
    if team_name not in admin_teams(registrations, request.user.email):
        raise PermissionDenied

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
    helper = AccreditationFormSetHelper()
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
    context = {
        "formset": formset,
        "team_name": team_name,
        "formset_helper": helper,
    }
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
