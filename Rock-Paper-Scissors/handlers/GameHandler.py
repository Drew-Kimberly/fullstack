"""
This file contains the class definition for the GameHandler controller class,
used by the Rock Paper Scissors application for handling logic related to
the Game entity.
"""


import random
from datetime import date
from models.Score import *
from models.User import *
from utils import *
from models.Game import *


ROUNDS_OPTIONS = [1, 3, 5, 7]
MOVES = ["ROCK", "PAPER", "SCISSORS"]


class GameHandler(object):
    """GameHandler service class"""

    def __init__(self):
        pass

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
        return game.to_form()

    @classmethod
    def get_game(cls, request):
        """Returns an existing game in the application"""
        # First verify the user is authenticated
        get_endpoints_current_user()

        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form()
        else:
            raise endpoints.NotFoundException('Game not found!')

    @classmethod
    def get_user_games(cls):
        """Returns all of the current User's active games"""
        gplus_user = get_endpoints_current_user()
        user = User.query(User.email == gplus_user.email()).get()

        active_games = Game.query() \
            .filter(Game.user == user.key) \
            .filter(Game.game_over == False)
        return GameForms(games=[game.to_form() for game in active_games])

    @classmethod
    def cancel_game(cls, request):
        """
        Removes a game that is currently in progress from the system. The game
        is specificed by Key, contained in the request, and must belong to the currently
        authenticated user.
        """
        # Get the current user - making sure it's authenticated
        gplus_user = get_endpoints_current_user()
        user = User.query(User.email == gplus_user.email()).get()

        # Get the game specified by key in the request
        game = get_by_urlsafe(request.urlsafe_game_key, Game)

        # Ensure the game exists
        if not game:
            raise endpoints.NotFoundException('Game not found!')

        # Ensure the game is associated to the current user
        if user.key != game.user:
            raise endpoints.ForbiddenException("Cannot cancel another user's game!")

        # Ensure the game is not completed
        if game.game_over:
            raise endpoints.ForbiddenException("Cannot cancel a game that has already been completed!")

        # All good to remove the game from datastore
        game.key.delete()

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
        game.cpu_moves.append(cpu_move)

        # Game logic to determine winner
        user_move = request.move.name
        game.user_moves.append(user_move)

        is_tie = False
        if cpu_move == user_move:
            is_tie = True
            game.user_won_last_round = None
            game.round_results.append(-1)
        elif user_move == "ROCK" and cpu_move == "SCISSORS":
            game.user_wins += 1
            game.user_won_last_round = True
            game.round_results.append(1)
        elif user_move == "PAPER" and cpu_move == "ROCK":
            game.user_wins += 1
            game.user_won_last_round = True
            game.round_results.append(1)
        elif user_move == "SCISSORS" and cpu_move == "PAPER":
            game.user_wins += 1
            game.user_won_last_round = True
            game.round_results.append(1)
        else:
            game.cpu_wins += 1
            game.user_won_last_round = False
            game.round_results.append(0)

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
            cls.end_game(game, game.user_wins > game.cpu_wins)

        # Update Game in datastore
        game.put()
        return game.to_form()

    @classmethod
    def get_game_history(cls, request):
        """
        Returns the round-by-round result of an active or completed Game.
        The game must be associated with the current authenticated user.
        """
        # Get the current user - making sure it's authenticated
        gplus_user = get_endpoints_current_user()
        user = User.query(User.email == gplus_user.email()).get()

        # Get the game specified by key in the request
        game = get_by_urlsafe(request.urlsafe_game_key, Game)

        # Ensure the game exists
        if not game:
            raise endpoints.NotFoundException('Game not found!')

        # Ensure the game is associated to the current user
        if user.key != game.user:
            raise endpoints.ForbiddenException("You may only view the history of your own games!")

        return game.to_gamehistory_form()

    @classmethod
    def end_game(cls, game, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        game.game_over = True
        game.put()

        # Add the game to the score 'board'
        score = Score(user=game.user, date=date.today(), won=won,
                      victory_margin=game.user_wins - game.cpu_wins)
        score.put()

        # Update the user's stats with the game result
        user = game.user.get()
        if won:
            user.num_wins += 1
        else:
            user.num_losses += 1
        user.total_victory_margin += (game.user_wins - game.cpu_wins)
        user.put()
