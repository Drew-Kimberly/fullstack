from flask import Flask, render_template, request, session, make_response, flash, redirect, url_for, jsonify
from AjaxHandler import AjaxHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import json
import httplib2
import requests
import random
import string


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)

engine = create_engine('postgresql:///catalog')
# engine = create_engine('mysql://andkim:andkim@localhost:3306/catalog', pool_recycle=3600)
Base.metadata.bind = engine

DBSessionMaker = sessionmaker(bind=engine)
dbSession = DBSessionMaker()
""":type: sqlalchemy.orm.Session"""


@app.route("/")
@app.route("/catalog", methods=["GET", "POST"])
def catalog():
    if request.method == 'POST':
        ajax_handler = AjaxHandler(dbSession)
        post_data = json.loads(request.form['request_data'])
        if post_data:
            if 'file_data' not in request.files:
                # Normal post request without uploaded file
                ajax_handler.posted_data = post_data
                response_data = ajax_handler.processRequest()  # ResponseData object
                if response_data:
                    return process_response(response_data)
                else:
                    return False
            else:
                # File included in request
                image_file = request.files['file_data']
                post_data = json.loads(request.form['request_data'])

                ajax_handler.posted_file = image_file
                ajax_handler.posted_data = post_data

                response_data = ajax_handler.processRequest()

                if response_data:
                    return process_response(response_data)
                else:
                    # Flash error message... return something better
                    return False
        else:
            # Bad POST request - No post data
            # Flash error message - Return something better
            return False
    else:
        categories = dbSession.query(Category).all()
        return render_template('catalog.html', categories=categories)


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    session['state'] = state
    return render_template("login.html", STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Exchange the one-time authorization code for a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in
    stored_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')
    if stored_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session['provider'] = 'google'
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']

    # If User doesn't exist, make a new one and add to database
    current_user_id = get_user_id(session.get('email'))
    if not current_user_id:
        # New User - First add to DB
        current_user_id = create_user(session)

    # Add the user_id to the session
    if current_user_id:
        session['user_id'] = current_user_id
        # Update appropriate user info stored in the database
        update_user(current_user_id)
    else:
        raise ValueError("Error adding the user's ID to the Session")

    flash("you are now logged in as %s" % session['username'])
    response = make_response(json.dumps("Success!"), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


# Revoke a current user's token and reset their login session.
@app.route("/gdisconnect")
def gdisconnect():
    # Only disconnect a connected user.
    access_token = session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Execute GET request to revoke current token.
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] != '200':
        # Token was invalid... for whatever reason
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token' \
          '&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # strip expire tag from access token
    token = result.split("&")[0]

    # Use token to get user info from API
    url = 'https://graph.facebook.com/v2.6/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    data = json.loads(result)

    session['provider'] = 'facebook'
    session['username'] = data["name"]
    session['email'] = data["email"]
    session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout,
    # let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = get_user_id(session['email'])
    if not user_id:
        user_id = create_user(session)

    if user_id:
        session['user_id'] = user_id
        # Update appropriate user info stored in the database
        update_user(user_id)
    else:
        raise ValueError("Error adding the user's ID to the Session")

    flash("Successfully Logged in as %s" % session['username'])
    response = make_response(json.dumps('Success'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/fbdisconnect')
def fbdisconnect():
    access_token = session.get('access_token')
    facebook_id = session.get('facebook_id')

    # Only disconnect a connected user
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    result = json.loads(result)
    if 'error' in result:
        response = make_response(json.dumps('Failed to revoke token for given user'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
def disconnect():
    if 'provider' in session:
        if session.get('provider') == 'google':
            gdisconnect()
            del session['gplus_id']
        if session.get('provider') == 'facebook':
            fbdisconnect()
            del session['facebook_id']
        del session['username']
        del session['email']
        del session['picture']
        del session['user_id']
        del session['access_token']
        del session['provider']
        flash("You have successfull been logged out.")
        return redirect(url_for('catalog'))
    else:
        flash("The user did not have an active logged in session!")
        return redirect(url_for('catalog'))


# JSON API Endpoint
@app.route('/catalog/api/getcatalog/json')
def getCatalog():
    catalog = []
    category_list = []
    categories = dbSession.query(Category).all()
    for category in categories:
        category_obj = category.serialize
        category_items = dbSession.query(Item).filter_by(category_id=category.category_id).all()
        item_list = []
        for item in category_items:
            item_obj = item.serialize
            if item.image_id:
                item_obj['image'] = item.image.serialize
            item_list.append(item_obj)
        category_obj['items'] = item_list
        category_list.append(category_obj)
    catalog.append({"categories": category_list})

    return json.dumps({"catalog": catalog})

# Helper Functions


# Processes the response_data object handed back by the AjaxHandler
# The workflow for processing responses is a major candidate to be
# refactored and improved using Flasks' make_response() method
def process_response(response_data):
    response = []
    for template in response_data.templates:
        if template:
            response.append(render_template(template, categories=response_data.categories, items=response_data.items))

    return json.dumps(response)


def create_user(user_session):
    try:
        newUser = User(
            name=user_session.get('username'),
            email=user_session.get('email'),
            picture=user_session.get('picture')
        )
        dbSession.add(newUser)
    except Exception as e:
        print(e.message)
        dbSession.rollback()
        return None

    dbSession.commit()
    user = dbSession.query(User).filter_by(email=user_session.get('email')).first()
    return user.user_id


def update_user(user_id):
    try:
        user = dbSession.query(User).filter_by(user_id=user_id).first()
        is_changed = False
        if user.name != session['username']:
            is_changed = True
            user.name = session['username']
        if user.picture != session['picture']:
            is_changed = True
            user.picture = session['picture']
        if is_changed:
            dbSession.add(user)
            dbSession.commit()
    except Exception as e:
        print(e.message + ' - when updating user info')
        dbSession.rollback()


def get_user_id(email):
    try:
        user = dbSession.query(User).filter_by(email=email).first()
        return user.user_id
    except Exception as e:
        print e.message
        return None


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
