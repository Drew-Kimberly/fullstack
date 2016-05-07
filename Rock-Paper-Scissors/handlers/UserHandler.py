"""
This file contains the class definition for the UserHandler controller class,
used by the Rock Paper Scissors application for handling logic related to
the User entity.
"""


from google.appengine.ext import ndb
from models.User import User, UserRankForms
from utils import get_endpoints_current_user


class UserHandler(object):
    """UserHandler service class"""

    def __init__(self):
        pass

    @classmethod
    def do_user_profile(cls, save_request=None):
        """
        Returns the User Profile. Will update User fields if
        request is passed in as argument.
        """
        user_profile = cls._get_user_profile()

        # Process changes made by user when saving the user profile
        if save_request:
            field = 'displayName'  # Currently the only updateable User field
            if hasattr(save_request, field):
                val = getattr(save_request, field)
                if val:
                    setattr(user_profile, field, str(val))
                    user_profile.put()

        return user_profile.to_form()

    @classmethod
    def get_user_rankings(cls, request):
        """
        Returns a list of UserRank forms ordered in descending order
        by total margin of victory.
        """
        # Ensure user is authenticated
        get_endpoints_current_user()

        users = User.query().order(-User.total_victory_margin)
        return UserRankForms(user_ranks=[user.to_rankform() for user in users])

    @staticmethod
    def _get_user_profile():
        """Returns User obj from datastore. Will create new one if non-existent."""
        # Ensure user is authenticated with Google+
        gplus_user = get_endpoints_current_user()

        # Attempt to get User from datastore
        user_id = gplus_user.email()
        user_key = ndb.Key(User, user_id)
        user = user_key.get()

        # Create new User in datastore if it doesn't exist
        if not user:
            user = User(
                key=user_key,
                displayName=gplus_user.nickname(),
                email=gplus_user.email()
            )
            user.put()

        return user
