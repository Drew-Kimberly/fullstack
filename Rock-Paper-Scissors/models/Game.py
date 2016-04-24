"""
This file contains the class definition for the Game datastore entity,
used by the Rock Paper Scissors application.
"""

import endpoints
import random

from datetime import date
from google.appengine.ext import ndb
from api_forms import GameForm
from Score import *
from User import *
from utils import *

ROUNDS_OPTIONS = [1, 3, 5, 7]
MOVES = ["ROCK", "PAPER", "SCISSORS"]


class Game(ndb.Model):
    """Game object"""
    total_rounds = ndb.IntegerProperty(required=True)
    remaining_rounds = ndb.IntegerProperty(required=True)
    user_wins = ndb.IntegerProperty(required=True, default=0)
    cpu_wins = ndb.IntegerProperty(required=True, default=0)
    game_over = ndb.BooleanProperty(required=True, default=False)
    user_last_move = ndb.StringProperty()
    cpu_last_move = ndb.StringProperty()
    user_won_last_round = ndb.BooleanProperty()
    total_ties = ndb.IntegerProperty(required=True, default=0)
    user = ndb.KeyProperty(required=True, kind='User')

    @classmethod
    def new_game(cls, request):
        """Creates and returns a new game"""
        gplus_user = get_endpoints_current_user()
        user = User.query(User.email == gplus_user.email()).get()

        if request.total_rounds not in ROUNDS_OPTIONS:
            raise endpoints.BadRequestException('Invalid total number of rounds.'
                                                ' Must be an odd number in the set [1,7].')

        game = Game(user=user.key, total_rounds=request.total_rounds, remaining_rounds=request.total_rounds)
        game.put()
        return cls._to_form(game)

    @classmethod
    def get_game(cls, request):
        """Returns an existing game in the application"""
        # First verify the user is authenticated
        get_endpoints_current_user()

        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return cls._to_form(game)
        else:
            raise endpoints.NotFoundException('Game not found!')

    @classmethod
    @ndb.transactional(xg=True)
    def play_round(cls, request):
        """
        Simulates a round of Rock Paper Scissors. Returns the current state of the
        game following the simulation.
        """
        # Make sure user is authenticated
        get_endpoints_current_user()

        # Grab the Game instance by the key
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if not game:
            raise endpoints.NotFoundException('Game not found!')

        # Ensure the game is not already completed
        if game.game_over:
            raise endpoints.BadRequestException('Game already over!')

        # Generate random move for the CPU
        cpu_move = random.choice(MOVES)

        # Game logic to determine winner
        user_move = request.move.name
        is_tie = False
        if cpu_move == user_move:
            is_tie = True
            game.user_won_last_round = None
        elif user_move == "ROCK" and cpu_move == "SCISSORS":
            game.user_wins += 1
            game.user_won_last_round = True
        elif user_move == "PAPER" and cpu_move == "ROCK":
            game.user_wins += 1
            game.user_won_last_round = True
        elif user_move == "SCISSORS" and cpu_move == "PAPER":
            game.user_wins += 1
            game.user_won_last_round = True
        else:
            game.cpu_wins += 1
            game.user_won_last_round = False

        # Handle ties - Only decrement the rounds remaining when the round is not a tie
        if is_tie:
            game.total_ties += 1
        else:
            game.remaining_rounds -= 1

        # Add the user and cpu moves to the game state
        game.user_last_move = user_move
        game.cpu_last_move = cpu_move

        # End the game if there is a winner
        rounds_to_win = (game.total_rounds / 2) + 1
        if game.cpu_wins == rounds_to_win or game.user_wins == rounds_to_win:
            game.end_game(game.user_wins > game.cpu_wins)

        # Update Game in datastore
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
        form.user_wins = game.user_wins
        form.cpu_wins = game.cpu_wins
        form.game_over = game.game_over
        form.user_last_move = game.user_last_move
        form.cpu_last_move = game.cpu_last_move
        form.user_won_last_round = game.user_won_last_round
        form.total_ties = game.total_ties
        return form

    def end_game(self, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()

        # Add the game to the score 'board'
        score = Score(user=self.user, date=date.today(), won=won,
                      victory_margin=self.user_wins - self.cpu_wins)
        score.put()
