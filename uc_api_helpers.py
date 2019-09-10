#!/usr/bin/python3

"""API helpers for Ultimate Central (indiaultimate.org)"""

import json
import os
import random

from faker import Faker
import requests


# Obtain this from https://upai.usetopscore.com/u/oauth-key
BASE_URL = "https://upai.usetopscore.com"
HEADERS = {}
HERE = os.path.dirname(os.path.abspath(__file__))


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

    url = "{}{}?event_id={}&fields[]=Person&fields[]=Team&per_page=1000".format(
        BASE_URL, "/api/registrations", event_id
    )

    for _ in range(retries):
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 200:
            data = r.json()
            break
        elif r.status_code == 403:
            _set_header_access_token()
        else:
            print("Response: {}".format(r))
        print("Retrying...")
    else:
        data = _fake_registration_data()

    return data


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
    response = requests.post("{}/api/oauth/server".format(BASE_URL), data=data)
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
    response = requests.post("{}/api/oauth/server".format(BASE_URL), data=data)
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
    r = requests.get(url)
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
    r = requests.get(url, headers=headers)
    info = r.json()["result"]
    if not info:
        return None
    return info[0]


if __name__ == "__main__":
    registrations = get_registrations("140982")
    for registration in registrations:
        print(registration)
