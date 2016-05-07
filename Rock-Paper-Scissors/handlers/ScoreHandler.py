"""
This file contains the class definition for the ScoreHandler controller class,
used by the Rock Paper Scissors application for handling logic related to
the Score entity.
"""


from models.User import *
from utils import *
from models.Score import *
from endpoints.api_exceptions import BadRequestException, NotFoundException


class ScoreHandler(object):
    """ScoreHandler service class"""

    def __init__(self):
        pass

    @classmethod
    def get_scores(cls):
        """Returns all Scores existing within the application."""
        # Check that user is authenticated
        get_endpoints_current_user()

        scores = Score.query()
        return ScoreForms(scores=[score.to_form() for score in scores])

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
        return ScoreForms(scores=[score.to_form() for score in scores])

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

        return ScoreForms(scores=[score.to_form() for score in scores])
