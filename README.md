# sotg-accreditation-tracker

## About
This web-app is used to track the [WFDF Rules
Accreditation](https://rules.wfdf.org/accreditation) of players participating in
the tournaments in India conducted by [UPAI](https://indiaultimate.org/).
Currently players are required to upload the certificate they recieve from WFDF.
The team the player is rostered with is fetched from UPAI and will allow players
and captains to view the all the accreditation status of their current roster.

The current webpage is [here](https://sotg-accreditation-tracker.herokuapp.com/)
and is showing some dummy information.

## Basic installation
This web-app is developed using Python (3.6) and
[Django](https://www.djangoproject.com/) and is deployed on
[Heroku](https://www.heroku.com/)

1. You need to have a working Python-3.6 installation.
1. Git clone this repo
1. Install all requirements in the repo using `pip install -r requirements.txt`.
   We recommend using a `virtualenv` for development.

## Deploying changes on Heroku
Once you have made changes to the local repo, deploying your changes to Heroku
should be as simple as pushing commits to Heroku via `git push heroku master`

You can view the current status of your deploy via 'heroku logs --tail'

## Contributions guidelines
Contributions welcome, please send us a pull request, or raise an issue.
