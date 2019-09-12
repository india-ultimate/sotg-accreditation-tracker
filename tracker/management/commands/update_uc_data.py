import json

import arrow
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError

from uc_api_helpers import get_registrations, get_tournaments


class Command(BaseCommand):
    help = "Update the caches with Ultimate Central data"

    def handle(self, *args, **options):
        tournaments = get_tournaments()

        print("Fetching data for tournaments to cache...")
        now = arrow.utcnow()
        for tournament in tournaments:
            end = arrow.get(tournament["end"])
            if end < now:
                continue
            event_id = tournament["id"]
            print("Caching event-{} registrations".format(event_id))
            key = "event-registrations-{}".format(event_id)
            registrations = get_registrations(event_id)
            if registrations:
                cache.set(key, json.dumps(registrations))
            print("Cached event-{} registrations".format(event_id))

        print("Updating tournament data in cache")
        if tournaments:
            cache.set("event-list", json.dumps(tournaments))
        print("Saved tournament data to cache")
