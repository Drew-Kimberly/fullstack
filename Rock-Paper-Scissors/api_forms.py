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


class NewGameForm(messages.Message):
    """Used to create a new game"""
    total_rounds = messages.IntegerField(1, required=True, default=3)


class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""
    guess = messages.IntegerField(1, required=True)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    guesses = messages.IntegerField(4, required=True)


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
