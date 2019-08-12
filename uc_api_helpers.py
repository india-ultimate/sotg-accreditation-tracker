#!/usr/bin/python3

"""API helpers for Ultimate Central (indiaultimate.org)"""

import json
import os

import requests


# Obtain this from https://upai.usetopscore.com/u/oauth-key
BASE_URL = "https://upai.usetopscore.com"
HEADER = {}


def set_header_access_token():
    CLIENT_ID = os.getenv("UPAI_CLIENT_ID")
    CLIENT_SECRET = os.getenv("UPAI_CLIENT_SECRET")
    assert CLIENT_ID, "Need to set UPAI_CLIENT_ID envvar"
    assert CLIENT_SECRET, "Need to set UPAI_CLIENT_SECRET envvar"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    response = requests.post("{}/api/oauth/server".format(BASE_URL), data=data)
    access_token = response.json()["access_token"]
    HEADER["Authorization"] = "Bearer {}".format(access_token)


def get_tournaments(year=None):
    url = "{}/api/events?per_page=100&order_by=date_desc".format(BASE_URL)
    r = requests.get(url)
    tournaments = r.json()["result"]
    if year is not None:
        tournaments = [
            t for t in tournaments if t["start"].startswith(str(year))
        ]
    return tournaments


def get_registrations(event_id=None, header=None):
    if header is None:
        # FIXME: Not necessary if access token already fetched
        set_header_access_token()
        header = HEADER

    url = "{}{}?event_id={}&fields[]=Person&fields[]=Team&per_page=1000".format(
        BASE_URL, "/api/registrations", event_id
    )
    r = requests.get(url, headers=header)
    registrations = r.json()["result"]

    def get_team_name(registration):
        return registration["Team"]["name"] if registration["Team"] else ""

    return sorted(registrations, key=get_team_name)


if __name__ == "__main__":
    registrations = get_registrations("140982")
    for registration in registrations:
        print(registration)
