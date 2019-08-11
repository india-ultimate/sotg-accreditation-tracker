from django.shortcuts import render, HttpResponse

from uc_api_helpers import get_registrations, get_tournaments

# FIXME: Move into events view
data = get_tournaments()
# FIXME: Move into event_page view
event_data = get_registrations(135604)


def home(request):
    return HttpResponse("Hello, World!")


def events(request):
    context = {"events": data}
    return render(request, "tracker/event-list.html", context)


def event_page(request, event_id):
    context = {"registrations": event_data}
    return render(request, "tracker/event-page.html", context)
