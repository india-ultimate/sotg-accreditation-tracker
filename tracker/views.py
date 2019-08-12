import json

from django.shortcuts import render, HttpResponse
from django.views.decorators.cache import cache_page
from django.conf import settings

from uc_api_helpers import get_registrations, get_tournaments


def home(request):
    return HttpResponse("Hello, World!")


def events(request):
    data = json.loads(_events_data(request).content)
    context = {"events": data}
    return render(request, "tracker/event-list.html", context)


def event_page(request, event_id):
    registrations = json.loads(_registrations_data(request, event_id).content)
    context = {"registrations": registrations}
    return render(request, "tracker/event-page.html", context)


@cache_page(60 * 15)
def _events_data(request):
    """Unexposed view to cache the tournament data

    The view is not exposed for users to directly access this data, but only
    exists for us to be able to piggyback on the Django cache infrastructure to
    cache the API responses, instead of writing our own caching code.

    """
    return HttpResponse(json.dumps(get_tournaments()))


@cache_page(60 * 15)
def _registrations_data(request, event_id):
    """Unexposed view to cache the registrations data

    The view is not exposed for users to directly access this data, but only
    exists for us to be able to piggyback on the Django cache infrastructure to
    cache the API responses, instead of writing our own caching code.

    """
    return HttpResponse(json.dumps(get_registrations(event_id)))
