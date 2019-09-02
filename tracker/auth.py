from django.contrib.auth.models import User

from uc_api_helpers import get_user


class TopScoreBackend:
    """Authenticate against the Top Score authentication."""

    def authenticate(self, request, username=None, password=None):
        user_info = get_user(username, password)
        if user_info is None:
            return None
        email, uc_username = user_info["email_address"], user_info["username"]
        first_name, last_name = user_info["first_name"], user_info["last_name"]
        teams = [team["name"] for team in user_info["teams"]]
        # FIXME: Put the uc_username and teams somewhere in the DB?
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Create a new user. There's no need to set a password we are
            # authenticating against Ultimate Central
            user = User(
                username=username, first_name=first_name, last_name=last_name
            )
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
