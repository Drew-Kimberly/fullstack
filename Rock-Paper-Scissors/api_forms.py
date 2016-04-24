"""
Defines the forms for the Rock-Paper-Scissors API that extend the
ProtoRPC message class.
"""

from protorpc import messages


class UserForm(messages.Message):
    """UserForm for information about the current user profile"""
    displayName = messages.StringField(1)
    email = messages.StringField(2)


class UserMiniForm(messages.Message):
    """UserMiniForm for updateable information about the current user"""
    displayName = messages.StringField(1)


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    total_rounds = messages.IntegerField(2, required=True)
    remaining_rounds = messages.IntegerField(3, required=True)
    game_over = messages.BooleanField(4, required=True)
    user_email = messages.StringField(5, required=True)
    user_name = messages.StringField(6, required=True)
    user_last_move = messages.StringField(7, required=True)
    cpu_last_move = messages.StringField(8, required=True)
    user_won_last_round = messages.BooleanField(9)
    total_ties = messages.IntegerField(10, required=True)
    user_wins = messages.IntegerField(11, required=True)
    cpu_wins = messages.IntegerField(12, required=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    total_rounds = messages.IntegerField(1, required=True, default=3)


class PlayRoundForm(messages.Message):
    """Used to make a move in an existing game"""
    move = messages.EnumField('GameMove', 1, required=True)


class GameMove(messages.Enum):
    """GameMove -- RPS move enumeration value"""
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_email = messages.StringField(1, required=True)
    user_name = messages.StringField(2, required=True)
    date = messages.StringField(3, required=True)
    won = messages.BooleanField(4, required=True)
    victory_margin = messages.IntegerField(5, required=True)


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
