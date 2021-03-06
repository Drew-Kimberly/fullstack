# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""


import endpoints
from protorpc import remote, messages, message_types

from handlers.GameHandler import GameHandler
from handlers.UserHandler import UserHandler
from handlers.ScoreHandler import ScoreHandler

from models.Game import GameForm, GameForms, GameHistoryForm, NewGameForm, PlayRoundForm, StringMessage
from models.User import UserForm, UserMiniForm, UserRankForms
from models.Score import ScoreForms

from settings import WEB_CLIENT_ID


GET_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1))
PLAY_ROUND_REQUEST = endpoints.ResourceContainer(
    PlayRoundForm,
    urlsafe_game_key=messages.StringField(1))
GET_USER_SCORES_REQUEST = endpoints.ResourceContainer(
    email=messages.StringField(1, required=True)
)
GET_HIGHSCORES_REQUEST = endpoints.ResourceContainer(
    number_of_results=messages.IntegerField(1, default=0)
)


EMAIL_SCOPE = endpoints.EMAIL_SCOPE
API_EXPLORER_CLIENT_ID = endpoints.API_EXPLORER_CLIENT_ID
MEMCACHE_MOVES_REMAINING = 'MOVES_REMAINING'


@endpoints.api(name='rock_paper_scissors', version='v1',
                    allowed_client_ids=[WEB_CLIENT_ID, API_EXPLORER_CLIENT_ID],
                    scopes=[EMAIL_SCOPE])
class RockPaperScissorsApi(remote.Service):
    """Game API"""

    @endpoints.method(request_message=UserMiniForm,
                      response_message=UserForm,
                      path='user',
                      name='save_user',
                      http_method='POST')
    def save_user(self, request):
        """Creates a new user profile if the sign in email does not exist in the system.
        Otherwise, updates the user profile's information if there is a change."""
        return UserHandler.do_user_profile(request)

    @endpoints.method(request_message=message_types.VoidMessage,
                      response_message=UserForm,
                      path='user',
                      name='get_user',
                      http_method='GET')
    def get_user(self, request):
        """Returns the current User profile."""
        return UserHandler.do_user_profile()

    @endpoints.method(request_message=NewGameForm,
                      response_message=GameForm,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Creates a new Rock-Paper-Scissors game"""
        return GameHandler.new_game(request)

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Return the current game state."""
        return GameHandler.get_game(request)

    @endpoints.method(request_message=PLAY_ROUND_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='play_round',
                      http_method='PUT')
    def play_round(self, request):
        """Plays a round. Returns a game state"""
        return GameHandler.play_round(request)

    @endpoints.method(response_message=ScoreForms,
                      path='scores',
                      name='get_scores',
                      http_method='GET')
    def get_scores(self, request):
        """Return all scores"""
        return ScoreHandler.get_scores()

    @endpoints.method(request_message=GET_USER_SCORES_REQUEST,
                      response_message=ScoreForms,
                      path='scores/user',
                      name='get_user_scores',
                      http_method='GET')
    def get_user_scores(self, request):
        """Returns all of the given User's scores"""
        return ScoreHandler.get_user_scores(request)

    @endpoints.method(request_message=message_types.VoidMessage,
                      response_message=GameForms,
                      path='user/games',
                      name='get_user_games',
                      http_method='GET')
    def get_user_games(self, request):
        """Returns all of the currently authenticated User's games"""
        return GameHandler.get_user_games()

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=StringMessage,
                      path='game/{urlsafe_game_key}',
                      name='cancel_game',
                      http_method='DELETE')
    def cancel_game(self, request):
        """Cancels an active game. The game must belong to current user."""
        GameHandler.cancel_game(request)
        return StringMessage(message='The game has been successfully cancelled!')

    @endpoints.method(request_message=GET_HIGHSCORES_REQUEST,
                      response_message=ScoreForms,
                      path='/highscores',
                      name='get_high_scores',
                      http_method='GET')
    def get_high_scores(self, request):
        """Returns a list of High Scores."""
        return ScoreHandler.get_high_scores(request)

    @endpoints.method(request_message=message_types.VoidMessage,
                      response_message=UserRankForms,
                      path='/user_rankings',
                      name='get_user_rankings',
                      http_method='GET')
    def get_user_rankings(self, request):
        """Returns a list of User Rankings, ordered by their total margin of victory."""
        return UserHandler.get_user_rankings(request)

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameHistoryForm,
                      path='game/{urlsafe_game_key}/history',
                      name='get_game_history',
                      http_method='GET')
    def get_game_history(self, request):
        """Returns the round-by-round result of an active or completed Game."""
        return GameHandler.get_game_history(request)


api = endpoints.api_server([RockPaperScissorsApi])
