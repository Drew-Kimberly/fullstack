"""
This file contains the class definition for the User datastore entity,
used by the Rock Paper Scissors application.
"""

from google.appengine.ext import ndb
from api_forms import UserForm
from api_forms import UserMiniForm
from utils import get_endpoints_current_user


class User(ndb.Model):
    """User -- User profile object"""
    displayName = ndb.StringProperty()
    email = ndb.StringProperty()

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

        return cls._to_form(user_profile)

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

    @staticmethod
    def _to_form(user_profile):
        """Copy fields from User model to UserForm RPC message"""
        user_form = UserForm()
        for field in user_form.all_fields():
            if hasattr(user_profile, field.name):
                setattr(user_form, field.name, getattr(user_profile, field.name))

        user_form.check_initialized()
        return user_form
