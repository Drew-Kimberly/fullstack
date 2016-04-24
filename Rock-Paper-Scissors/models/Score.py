"""
This file contains the class definition for the Score datastore entity,
used by the Rock Paper Scissors application.
"""

from google.appengine.ext import ndb
from models.User import User
from api_forms import ScoreForm, ScoreForms
from utils import get_endpoints_current_user
from endpoints.api_exceptions import NotFoundException
from endpoints.api_exceptions import BadRequestException


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

    @classmethod
    def get_user_scores(cls, request):
        """Returns all Scores associated with the current signed-in User"""
        # Check that current user is authenticated
        get_endpoints_current_user()

        user = User.query(User.email == request.email).get()
        if not user:
            raise NotFoundException(
                'A User with that email address does not exist!')

        scores = Score.query(Score.user == user.key)
        return cls._to_forms([cls._to_form(score) for score in scores])

    @classmethod
    def get_high_scores(cls, request):
        """
        Returns a list of highscores. The scores are ordered
        in descending order by the margin of victory. In the request,
        the user can specify 'number_of_results' to limit the total
        number of scores returned
        """
        # Check that the current user is authenticated
        get_endpoints_current_user()

        # Get number_of_results limit from request
        number_of_results = request.number_of_results

        if number_of_results < 0:
            raise BadRequestException("Number of results field must be greater than 0!")
        elif number_of_results == 0:
            scores = Score.query().order(-Score.victory_margin)
        else:
            scores = Score.query().order(-Score.victory_margin).fetch(number_of_results)

        return cls._to_forms([cls._to_form(score) for score in scores])

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
