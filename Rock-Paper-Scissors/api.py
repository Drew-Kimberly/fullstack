# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""


import logging
import endpoints

from protorpc import remote
from protorpc import messages
from protorpc import message_types

from google.appengine.api import memcache
from google.appengine.api import taskqueue

from models.User import *
from models.Game import *
from models.Score import *

from api_forms import NewGameForm, PlayRoundForm, ScoreForms, StringMessage, UserMiniForm
from settings import WEB_CLIENT_ID


GET_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1),)
PLAY_ROUND_REQUEST = endpoints.ResourceContainer(
    PlayRoundForm,
    urlsafe_game_key=messages.StringField(1),)

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
        return User.do_user_profile(request)

    @endpoints.method(request_message=message_types.VoidMessage,
                      response_message=UserForm,
                      path='user',
                      name='get_user',
                      http_method='GET')
    def get_user(self, request):
        """Returns the current User profile."""
        return User.do_user_profile()

    @endpoints.method(request_message=NewGameForm,
                      response_message=GameForm,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Creates a new Rock-Paper-Scissors game"""

        # Use a task queue to update the average attempts remaining.
        # This operation is not needed to complete the creation of a new game
        # so it is performed out of sequence.
        # taskqueue.add(url='/tasks/cache_average_attempts')
        return Game.new_game(request)

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Return the current game state."""
        return Game.get_game(request)

    @endpoints.method(request_message=PLAY_ROUND_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='play_round',
                      http_method='PUT')
    def play_round(self, request):
        """Plays a round. Returns a game state"""
        return Game.play_round(request)

    @endpoints.method(response_message=ScoreForms,
                      path='scores',
                      name='get_scores',
                      http_method='GET')
    def get_scores(self, request):
        """Return all scores"""
        return ScoreForms(items=[score.to_form() for score in Score.query()])

    @endpoints.method(request_message=UserForm,
                      response_message=ScoreForms,
                      path='scores/user/{user_name}',
                      name='get_user_scores',
                      http_method='GET')
    def get_user_scores(self, request):
        """Returns all of an individual User's scores"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        scores = Score.query(Score.user == user.key)
        return ScoreForms(items=[score.to_form() for score in scores])

    @endpoints.method(response_message=StringMessage,
                      path='games/average_attempts',
                      name='get_average_attempts_remaining',
                      http_method='GET')
    def get_average_attempts(self, request):
        """Get the cached average moves remaining"""
        return StringMessage(message=memcache.get(MEMCACHE_MOVES_REMAINING) or '')

    @staticmethod
    def _cache_average_attempts():
        """Populates memcache with the average moves remaining of Games"""
        games = Game.query(Game.game_over == False).fetch()
        if games:
            count = len(games)
            total_attempts_remaining = sum([game.attempts_remaining
                                            for game in games])
            average = float(total_attempts_remaining)/count
            memcache.set(MEMCACHE_MOVES_REMAINING,
                         'The average moves remaining is {:.2f}'.format(average))


api = endpoints.api_server([RockPaperScissorsApi])
