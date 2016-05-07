"""
This file contains the class definition for the Score datastore entity,
used by the Rock Paper Scissors application.
"""

from google.appengine.ext import ndb
from protorpc import messages


class Score(ndb.Model):
    """Rock-Paper-Scissors Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    victory_margin = ndb.IntegerProperty(required=True)

    def to_form(self):
        """Converts a Score ndb instance into a ScoreForm RPC message"""
        return ScoreForm(
            user_email=self.user.get().email,
            user_name=self.user.get().displayName,
            won=self.won,
            date=str(self.date),
            victory_margin=self.victory_margin
        )


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_email = messages.StringField(1, required=True)
    user_name = messages.StringField(2, required=True)
    date = messages.StringField(3, required=True)
    won = messages.BooleanField(4, required=True)
    victory_margin = messages.IntegerField(5, required=True)


class ScoreForms(messages.Message):
    """Return multiple ScoreForm's"""
    scores = messages.MessageField(ScoreForm, 1, repeated=True)