"""utils.py - File for collecting general utility functions."""

import logging
from google.appengine.ext import ndb
import endpoints


# Source: https://github.com/GoogleCloudPlatform/appengine-endpoints-tictactoe-python
def get_endpoints_current_user(raise_unauthorized=True):
    """Returns a current user and (optionally) causes an HTTP 401 if no user.
    Args:
        raise_unauthorized: Boolean; defaults to True. If True, this method
            raises an exception which causes an HTTP 401 Unauthorized to be
            returned with the request.
    Returns:
        The signed in user if there is one, else None if there is no signed in
        user and raise_unauthorized is False.
    """
    current_user = endpoints.get_current_user()
    if raise_unauthorized and current_user is None:
        raise endpoints.UnauthorizedException('Invalid token - Must be authenticated to perform this action.')
    return current_user


def get_by_urlsafe(urlsafe, model):
    """Returns an ndb.Model entity that the urlsafe key points to. Checks
        that the type of entity returned is of the correct kind. Raises an
        error if the key String is malformed or the entity is of the incorrect
        kind
    Args:
        urlsafe: A urlsafe key string
        model: The expected entity kind
    Returns:
        The entity that the urlsafe Key string points to or None if no entity
        exists.
    Raises:
        ValueError:"""
    try:
        key = ndb.Key(urlsafe=urlsafe)
    except TypeError:
        raise endpoints.BadRequestException('Invalid Key')
    except Exception as e:
        if e.__class__.__name__ == 'ProtocolBufferDecodeError':
            raise endpoints.BadRequestException('Invalid Key')
        else:
            raise
    try:
        entity = key.get()
    except Exception as e:
        return None

    if not entity:
        return None

    if not isinstance(entity, model):
        raise ValueError('Incorrect Kind')
    return entity


def get_user_id(user, id_type="email"):
    """Returns the user_id for the given User"""
    if id_type == "email":
        return user.email()

    if id_type == "oauth":
        """A workaround implementation for getting userid."""
        auth = os.getenv('HTTP_AUTHORIZATION')
        bearer, token = auth.split()
        token_type = 'id_token'
        if 'OAUTH_USER_ID' in os.environ:
            token_type = 'access_token'
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?%s=%s'
               % (token_type, token))
        user = {}
        wait = 1
        for i in range(3):
            resp = urlfetch.fetch(url)
            if resp.status_code == 200:
                user = json.loads(resp.content)
                break
            elif resp.status_code == 400 and 'invalid_token' in resp.content:
                url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?%s=%s'
                       % ('access_token', token))
            else:
                time.sleep(wait)
                wait = wait + i
        return user.get('user_id', '')