"""
This file contains the class definition for the Game datastore entity,
used by the Rock Paper Scissors application.
"""

import endpoints

from datetime import date
from google.appengine.ext import ndb
from api_forms import GameForm
from Score import *
from User import *
from utils import get_endpoints_current_user

ROUNDS_OPTIONS = [1, 3, 5, 7]


class Game(ndb.Model):
    """Game object"""
    total_rounds = ndb.IntegerProperty(required=True)
    remaining_rounds = ndb.IntegerProperty(required=True)
    user_wins = ndb.IntegerProperty(required=True, default=0)
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')

    @classmethod
    def new_game(cls, request):
        """Creates and returns a new game"""
        gplus_user = get_endpoints_current_user()
        user = User.query(User.email == gplus_user.email()).get()

        if request.total_rounds not in ROUNDS_OPTIONS:
            raise endpoints.BadRequestException('Invalid total number of rounds. Must be an odd number in the set [1,7].')

        game = Game(user=user.key, total_rounds=request.total_rounds, remaining_rounds=request.total_rounds)
        game.put()
        return cls._to_form(game)

    @staticmethod
    def _to_form(game):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = game.key.urlsafe()
        form.user_email = game.user.get().email
        form.user_name = game.user.get().displayName
        form.total_rounds = game.total_rounds
        form.remaining_rounds = game.remaining_rounds
        form.game_over = game.game_over
        return form

    def end_game(self, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()
        # Add the game to the score 'board'
        score = Score(user=self.user, date=date.today(), won=won,
                      guesses=self.attempts_allowed - self.attempts_remaining)
        score.put()
