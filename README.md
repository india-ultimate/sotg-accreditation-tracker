# sotg-accreditation-tracker

## About

<!-- This section is also displayed in the index view. Use pure HTML here! -->

<p>This webapp is used to track the <a
href="https://rules.wfdf.org/accreditation">WFDF Rules Accreditation</a> of
players participating in the tournaments in India conducted by the <a
href="https://indiaultimate.org">UPAI</a></p>

<p>Captains and Admins of teams can login using their India Ultimate login
credentials and upload accreditation information for the players participating
in a tournament on their team. Admins can fill-in the information in batches, as
and when they are able to collect information from the players.</p>

<p>Each event has a page that displays the accreditation status of all players
participating in the tournament, along with some team-wise statistics. Event
co-ordinators and SOTG committee can audit the accreditation information by
looking at each events' page.</p>

## Basic installation
This web-app is developed using Python (3.6) and
[Django](https://www.djangoproject.com/) and is deployed on
[Heroku](https://www.heroku.com/)

1. You need to have a working Python-3.6 installation.
1. Git clone this repo
1. Install all requirements in the repo using `pip install -r requirements.txt`.
   We recommend using a `virtualenv` for development.
1. Once you have the requirements installed, you can run the app using `python
   manage.py runserver`.
1. To work on some of the login based views, you need to have a local user
   account if you don't have a Ultimate Central keys set in the environment. You
   can create a superuser account using `python manage.py createsuperuser`.

## Deploying changes on Heroku
Once you have made changes to the local repo, deploying your changes to Heroku
should be as simple as pushing commits to Heroku via `git push heroku master`

You can view the current status of your deploy via 'heroku logs --tail'

## Contributions guidelines
Contributions welcome, please send us a pull request, or raise an issue.
