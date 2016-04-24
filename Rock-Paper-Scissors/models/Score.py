"""
This file contains the class definition for the Score datastore entity,
used by the Rock Paper Scissors application.
"""

from google.appengine.ext import ndb
from api_forms import ScoreForm


class Score(ndb.Model):
    """Rock-Paper-Scissors Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    victory_margin = ndb.IntegerProperty(required=True)

    def to_form(self):
        """"""
        return ScoreForm(
            user_email=self.user.get().email,
            user_name=self.user.get().displayName,
            won=self.won,
            date=str(self.date),
            victory_margin=self.victory_margin
        )
