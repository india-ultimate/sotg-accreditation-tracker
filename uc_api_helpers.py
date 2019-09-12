#!/usr/bin/python3

"""API helpers for Ultimate Central (indiaultimate.org)"""

import json
import os
import random
from urllib.parse import parse_qsl, urlencode

from faker import Faker
from requests import Session

# Obtain this from https://upai.usetopscore.com/u/oauth-key
BASE_URL = "https://upai.usetopscore.com"
HEADERS = {}
HERE = os.path.dirname(os.path.abspath(__file__))
session = Session()


def _fake_registration_data():
    """Return fake data when the user doesn't have access to the API"""
    data = {
        "action": "api_registrations_list",
        "status": 200,
        "count": 20,
        "result": _generate_registrations(),
    }
    return data


def _fetch_registration_data(event_id, retries=2):
    """Fetch registration data for the specified event.

    We try to fetch the data once without refreshing the access_token, and on
    failure, once after refreshing the access token. If we fail after that,
    random data is used as a response.

    """

    url = "{}{}?event_id={}&fields[]=Person&fields[]=Team&per_page=1000&page=1".format(
        BASE_URL, "/api/registrations", event_id
    )

    for _ in range(retries):
        r = session.get(url, headers=HEADERS)
        if r.status_code == 200:
            data = _fetch_all_data(url, r)
            break
        elif r.status_code == 403:
            _set_header_access_token()
        else:
            print("Response: {}".format(r))
        print("Retrying...")
    else:
        data = (
            _fake_registration_data()
            if "NO_FAKE_DATA" not in os.environ
            else {"result": []}
        )

    return data


def _fetch_all_data(url, first_response):
    data = first_response.json()
    if data["count"] == len(data["result"]):
        return data

    else:
        url = _next_page(url)
        retries = 3
        while len(data["result"]) < data["count"] and retries > 0:
            print(url)
            r = session.get(url, headers=HEADERS)
            if r.status_code == 200:
                data["result"].extend(r.json()["result"])
                url = _next_page(url)
            else:
                retries -= 1
        return data


def _next_page(url):
    """Return URL of the next page."""

    base, qs = url.split("?")
    parsed = parse_qsl(qs)
    page = int(dict(parsed)["page"]) + 1
    parsed = [(key, value if key != "page" else page) for key, value in parsed]
    return "{}?{}".format(base, urlencode(parsed))


def _generate_registrations(n=20):
    faker = Faker()
    roles = ["player", "admin", "captain"]
    teams = [{"name": faker.company()} for _ in range(n // 5)]
    teams.insert(0, None)

    def get_registration():
        registration = {
            # More fields can be added to the dummy data based on
            # https://upai.usetopscore.com/api/help?endpoint=%2Fapi%2Fregistrations
            # https://upai.usetopscore.com/api/help?endpoint=%2Fapi%2Fteams
            # https://upai.usetopscore.com/api/help?endpoint=%2Fapi%2Fpersons
            "role": random.choice(roles),
            "Team": random.choice(teams),
            "Person": {
                "full_name": faker.name(),
                "email_address": faker.email(),
                "slug": faker.slug(),
            },
        }
        return registration

    return [get_registration() for _ in range(n)]


def _get_user_access_token(username, password):
    CLIENT_ID = os.getenv("UPAI_CLIENT_ID")
    CLIENT_SECRET = os.getenv("UPAI_CLIENT_SECRET")
    data = {
        "grant_type": "password",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": username,
        "password": password,
    }
    print("Fetching access token")
    response = session.post("{}/api/oauth/server".format(BASE_URL), data=data)
    if response.status_code != 200:
        print("Could not fetch access token")
        return

    return response.json()["access_token"]


def _set_header_access_token():
    CLIENT_ID = os.getenv("UPAI_CLIENT_ID")
    CLIENT_SECRET = os.getenv("UPAI_CLIENT_SECRET")
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    print("Fetching access token")
    response = session.post("{}/api/oauth/server".format(BASE_URL), data=data)
    if response.status_code != 200:
        print("Could not fetch access token")
        return

    access_token = response.json()["access_token"]
    HEADERS["Authorization"] = "Bearer {}".format(access_token)


# API Helpers ####


def get_registrations(event_id=None):
    data = _fetch_registration_data(event_id)
    registrations = data["result"]

    def get_team_name(registration):
        return registration["Team"]["name"] if registration["Team"] else ""

    return sorted(registrations, key=get_team_name)


def get_tournaments(year=None):
    url = "{}/api/events?per_page=100&order_by=date_desc".format(BASE_URL)
    r = session.get(url)
    tournaments = r.json()["result"]
    if year is not None:
        tournaments = [
            t for t in tournaments if t["start"].startswith(str(year))
        ]
    return tournaments


def get_user(username, password):
    access_token = _get_user_access_token(username, password)
    headers = {"Authorization": "Bearer {}".format(access_token)}
    url = "{}/api/persons/me".format(BASE_URL)
    r = session.get(url, headers=headers)
    info = r.json()["result"]
    if not info:
        return None
    return info[0]


if __name__ == "__main__":
    registrations = get_registrations("140982")
    for registration in registrations:
        print(registration)
