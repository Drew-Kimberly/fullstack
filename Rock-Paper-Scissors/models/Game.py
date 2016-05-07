"""
This file contains the class definition for the Game datastore entity,
used by the Rock Paper Scissors application.
"""
from __builtin__ import classmethod

from protorpc import messages
from google.appengine.ext import ndb


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
    user_moves = ndb.StringProperty(repeated=True)
    cpu_moves = ndb.StringProperty(repeated=True)
    round_results = ndb.IntegerProperty(repeated=True)
    user = ndb.KeyProperty(required=True, kind='User')

    def to_form(self):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_email = self.user.get().email
        form.user_name = self.user.get().displayName
        form.total_rounds = self.total_rounds
        form.remaining_rounds = self.remaining_rounds
        form.user_wins = self.user_wins
        form.cpu_wins = self.cpu_wins
        form.game_over = self.game_over
        form.user_last_move = self.user_last_move
        form.cpu_last_move = self.cpu_last_move
        form.user_won_last_round = self.user_won_last_round
        form.total_ties = self.total_ties
        return form

    def to_gamehistory_form(self):
        """Returns a GameHistoryForm RPC message from a Game entity"""
        rounds = []
        for i in range(len(self.user_moves)):
            form = RoundHistoryForm()
            form.user_move = self.user_moves[i]
            form.cpu_move = self.cpu_moves[i]
            if self.round_results[i] == -1:
                form.is_tie = True
                form.user_won = False
            elif self.round_results[i] == 0:
                form.is_tie = False
                form.user_won = False
            else:
                form.is_tie = False
                form.user_won = True

            rounds.append(form)

        return GameHistoryForm(game_history=rounds)


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    total_rounds = messages.IntegerField(2, required=True)
    remaining_rounds = messages.IntegerField(3, required=True)
    game_over = messages.BooleanField(4, required=True)
    user_email = messages.StringField(5, required=True)
    user_name = messages.StringField(6, required=True)
    user_last_move = messages.StringField(7)
    cpu_last_move = messages.StringField(8)
    user_won_last_round = messages.BooleanField(9)
    total_ties = messages.IntegerField(10, required=True)
    user_wins = messages.IntegerField(11, required=True)
    cpu_wins = messages.IntegerField(12, required=True)


class GameForms(messages.Message):
    """Return multiple GameForm's"""
    games = messages.MessageField(GameForm, 1, repeated=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    total_rounds = messages.IntegerField(1, required=True, default=3)


class RoundHistoryForm(messages.Message):
    """RoundHistoryForm for summarizing an already completed round."""
    user_move = messages.StringField(1, required=True)
    cpu_move = messages.StringField(2, required=True)
    user_won = messages.BooleanField(3, required=True, default=False)
    is_tie = messages.BooleanField(4, required=True, default=False)


class GameHistoryForm(messages.Message):
    """Consists of multiple RoundHistoryForm's to create a game history."""
    game_history = messages.MessageField(RoundHistoryForm, 1, repeated=True)


class GameMove(messages.Enum):
    """GameMove -- RPS move enumeration value"""
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class PlayRoundForm(messages.Message):
    """Used to make a move in an existing game"""
    move = messages.EnumField('GameMove', 1, required=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
