"""
This file contains the class definition for the User datastore entity,
used by the Rock Paper Scissors application.
"""


from protorpc import messages
from google.appengine.ext import ndb


class User(ndb.Model):
    """User -- User profile object"""
    displayName = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    num_wins = ndb.IntegerProperty(required=True, default=0)
    num_losses = ndb.IntegerProperty(required=True, default=0)
    total_victory_margin = ndb.IntegerProperty(required=True, default=0)

    def to_form(self):
        """Copy fields from User model to UserForm RPC message"""
        user_form = UserForm()
        for field in user_form.all_fields():
            if hasattr(self, field.name):
                setattr(user_form, field.name, getattr(self, field.name))

        user_form.check_initialized()
        return user_form

    def to_rankform(self):
        """Given a User entity, returns a UserRankForm RPC message"""
        user_rank_form = UserRankForm()
        for field in user_rank_form.all_fields():
            if hasattr(self, field.name):
                setattr(user_rank_form, field.name, getattr(self, field.name))

        user_rank_form.check_initialized()
        return user_rank_form


class UserForm(messages.Message):
    """UserForm for information about the current user profile"""
    displayName = messages.StringField(1)
    email = messages.StringField(2)
    num_wins = messages.IntegerField(3, default=0)
    num_losses = messages.IntegerField(4, default=0)
    total_victory_margin = messages.IntegerField(5, default=0)


class UserMiniForm(messages.Message):
    """UserMiniForm for updateable information about the current user"""
    displayName = messages.StringField(1)


class UserRankForm(messages.Message):
    """UserRankForm for outbound individual user ranking information"""
    email = messages.StringField(1, required=True)
    displayName = messages.StringField(2, required=True)
    total_victory_margin = messages.IntegerField(3, required=True, default=0)


class UserRankForms(messages.Message):
    """Return multiple UserRankForm's"""
    user_ranks = messages.MessageField(UserRankForm, 1, repeated=True)
