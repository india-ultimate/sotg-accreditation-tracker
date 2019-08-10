from django.shortcuts import render, HttpResponse

from uc_api_helpers import get_tournaments

# FIXME: Move into events view
data = get_tournaments()


def home(request):
    return HttpResponse("Hello, World!")


def events(request):
    context = {"events": data}
    return render(request, "tracker/event-list.html", context)
