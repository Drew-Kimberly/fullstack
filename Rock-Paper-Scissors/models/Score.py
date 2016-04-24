"""
This file contains the class definition for the Score datastore entity,
used by the Rock Paper Scissors application.
"""

from google.appengine.ext import ndb
from api_forms import ScoreForm, ScoreForms
from utils import get_endpoints_current_user


class Score(ndb.Model):
    """Rock-Paper-Scissors Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    victory_margin = ndb.IntegerProperty(required=True)

    @classmethod
    def get_scores(cls):
        """Returns all Scores existing within the application."""
        # Check that user is authenticated
        get_endpoints_current_user()

        scores = [cls._to_form(score) for score in Score.query()]
        return cls._to_forms(scores)

    @staticmethod
    def _to_form(score):
        """Converts a Score ndb instance into a ScoreForm RPC message"""
        return ScoreForm(
            user_email=score.user.get().email,
            user_name=score.user.get().displayName,
            won=score.won,
            date=str(score.date),
            victory_margin=score.victory_margin
        )

    @staticmethod
    def _to_forms(scores):
        """Converts an array of Score ndb instances into a ScoreForms RPC message."""
        return ScoreForms(scores=scores)
