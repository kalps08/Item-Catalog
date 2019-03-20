import json
# use these to create a pseudo-random string that identifies each session
import random
import string

# a comprehensive HTTP client library in Python
import httplib2
import requests
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import make_response
# this login_session object acts like a dictionary - store values in it
# for the longevity of a user's session with our server
from flask import session as login_session
from oauth2client.client import FlowExchangeError
# IMPORTS for g_connect
from oauth2client.client import flow_from_clientsecrets
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

from models import Base, Category, Item, User

# NEW IMPORTS FOR THIS STEP

app = Flask(__name__)

# declare my client ID by referencing this clients_secrets json file
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"

# Connect to Database and create database session
# engine = create_engine('sqlite:///item-catalog.db', connect_args={'check_same_thread': False})
engine = create_engine('postgresql://catalog:yourPassword@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# CREATE ANTI-FORGERY STATE TOKEN WITH EACH GET REQUEST TO THE SERVER
@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Server side facebook login handler
@app.route('/fb_connect', methods=['POST'])
def fb_connect():
    # Verify value of State token to protect against croos-site reference forgery attacks.
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Exchange short-lived token for a long-lived token
    access_token = request.data
    # have to send app-secret to facebook to verify the server identity
    # app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
    app_id = json.loads(open('/var/www/catalog/Item-Catalog/fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?' \
          'grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' \
          % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API - tokens come with expiry date - long token upto two months
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    # verify that we can make API calls with this new token
    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    # and populate login_session
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture - Facebook uses a separate API call to retrieve a profile picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;' \
              'border-radius: 150px;-webkit-border-radius: 150px;' \
              '-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    print(output)
    return output


# server-side function to handle the callback function
@app.route('/g_connect', methods=['POST'])
def g_connect():
    # -------------------------
    # State Tokens Match Check
    # -------------------------

    # Validate state token --- confirm that the token that the client sends to
    # the server matches the token that the server sent to the client
    # this round-trip verification helps ensure that the user is making the request not a malicious script
    # using the request.args.get() method, the code examines the state token passed in and compares to the
    # state of the login session.
    if request.args.get('state') != login_session['state']:
        # if they don't match, then create a response of an invalid state token and return this message to the client.
        # no further auth will occur on server side if these two state tokens dont match
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code -- if the state tokens match, then proceed by collecting the one-time code from
    # the server with the request.data function.
    code = request.data

    # ------------------------------------------------------------
    # Exchange One-time code for an Access Token from Google API
    # ------------------------------------------------------------

    try:
        # Upgrade the authorization code into a credentials object
        # use the one-time code and exchange it for a credentials object which will contain the
        # access token for my server
        # this line contains the oauth flow object and adds my client's secret key info to it
        scopes = ['https://www.googleapis.com/auth/userinfo.email',
                  'https://www.googleapis.com/auth/userinfo.profile']
        # oauth_flow = flow_from_clientsecrets('client_secret.json', scope='') - does not return name
        # oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        # oauth_flow = flow_from_clientsecrets('client_secrets.json', scopes)
        oauth_flow = flow_from_clientsecrets('/var/www/catalog/Item-Catalog/client_secrets.json', scopes)

        # here, specify with post message that this is the one time code flow the server will be sending off.
        oauth_flow.redirect_uri = 'postmessage'
        # finally, initiate the exchange with the step2_exchange() function passing in my one-time code as input
        # this step2_exchange() function of the flow class exchanges an authorization code for a credentials object
        # if all goes well, response from Google will be an object stored under the name credentials
        credentials = oauth_flow.step2_exchange(code)
        # if error happens along the way, then throw a flow exchange error and send the response as JSON object.
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # --------------------------------
    # Verify if working Access Token
    # --------------------------------

    # Check if there's a valid access token inside of the credentials object and store it in access_token variable.
    access_token = credentials.access_token
    # append it to the following Google URL, the Google API server can verify if its a valid token for use.
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Create a json GET request containing the URL and access
    # token and store the results of this request in "result" variable.
    h = httplib2.Http()
    http_response = h.request(url, 'GET')
    result = json.loads(http_response[1])
    # If the result was an error in the access token info, abort -- send a 500 Internal Server Error to the client
    # but if no error, then we know that we have a working
    # access token but we need to make sure we have the right access token.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # -------------------------------------------------
    # Verify if right Access Token matching User's ID
    # -------------------------------------------------

    # Verify that the access token is used for the intended user.
    # grab the ID of the token in my credentials object and compare to the ID returned by the Google API server.
    # if the two IDs don't match, we do not have the correct token - so don't allow
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # -----------------------------------------------------------
    # Verify if Access Token has correct client ID for this app
    # -----------------------------------------------------------

    # Verify that the access token is valid for this app.
    # if the two Client IDs don't match, our app is trying to use a client ID that
    # does not belong to it - so don't allow
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response
    # ----------------------------------
    # Verify if user already logged in
    # ----------------------------------

    # Verify is user is already logged in
    # If already logged in, return a 200 successful authentication without resetting all
    # the login session variables again
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Assuming all the checks (above IF statements) were fine, we have a user who can successfully login to our server
    # using google api credentials - In this user login session, store their credentials in Google Plus ID
    login_session['access_token'] = credentials.access_token
    login_session['provider'] = 'google'
    login_session['gplus_id'] = gplus_id

    # Get user info - by sending a message to Google Plus API using the access token,
    # as allowed by the token scope in "data" object
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    # user's info from google plus api
    data = answer.json()
    # data = json.loads(answer.text)

    # Store the params in login_session object, that we are interested in from the data object (user info)
    login_session['username'] = data['email']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Check if user exists, if not make a new one
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    # Send out a response to the client showing user's name, picture and a flash messsage showing they are logged in
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '; email: ' + login_session['email']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;' \
              '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    # flash("You are now logged in as %s" % login_session['username'])
    flash("You are now logged in as {}".format(login_session['username']))
    return output


# common disconnect function for any oauth provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']

        # clear login_session variable
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have been successfully logged out!")
        return redirect(url_for('show_latest_items'))
    else:
        flash("You were not logged in to begin with!")
        return redirect(url_for('show_latest_items'))


# this function - to reject the access token when the user's ready to logout
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# User Helper Functions
def create_user(login_session):
    new_user = User(name=login_session['username'], email=login_session['email'],
                    picture=login_session['picture'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_info_by_id(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user


def get_user_info_by_emaild(email):
    user = session.query(User).filter_by(email=email).first()
    return user


def get_user_id(email):
    user = session.query(User).filter_by(email=email).first()
    return user.id


# Show all Categories
@app.route('/')
@app.route('/home')
@app.route('/catalog')
def show_latest_items():
    """
        * Render homepage
        * Show categories on the left, and latest items in middle
        * Home page of the application
    """

    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Item).order_by(asc(Item.id)).limit(5)
    item_categories = session.query(Item, User, Category).filter(Category.id == Item.cat_id).filter(
        Item.user_id == User.id).limit(5)
    categories_list = session.query(Category).order_by(asc(Category.name)).all()

    full_info = list()
    for a, b, c in item_categories:
        info = (a.title, a.id, b.name, c.name)
        full_info.append(info)

    # Check if user is logged in to enable add new item button
    if 'username' in login_session:
        user_authorized = True
    else:
        user_authorized = False
    return render_template('itemsList.html',
                           categories=categories,
                           items=items,
                           full_info=full_info,
                           user_authorized=user_authorized)


# Show Items for a Category
@app.route('/catalog/<category_name>/items')
def show_items_for_category(category_name):
    """
        Generate page to show all items for the selected category
    """
    cat_name = ""
    if str(request.args.get('category_name')) is not None:
        cat_name = category_name.encode("utf-8")

    categories = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(name=cat_name).first()

    user = get_user_info_by_id(category.user_id)
    items = session.query(Item).filter_by(cat_id=category.id).all()

    # Check if user is logged in to enable add new item button
    if 'username' in login_session:
        user_authorized = True
    else:
        user_authorized = False
    return render_template('itemsList.html',
                           categories=categories,
                           items=items,
                           cat_name=cat_name,
                           user_authorized=user_authorized)


# Show Item Description for selected Item
@app.route('/catalog/<category_name>/<item_id>/<item_name>')
def show_item_description(category_name, item_id, item_name):
    """
        Generate page to show the description of the selected item
        Enable edit/delete features for a logged user only if he
        owns/created the item
    """

    if str(request.args.get('category_name')) is not None:
        cat_name = category_name.encode("utf-8")
    if str(request.args.get('item_name')) is not None:
        item_name = item_name.encode("utf-8")

    item = session.query(Item).filter_by(id=item_id).first()
    user = get_user_info_by_id(item.user_id)

    # Check if user is logged in and also check if he owns the item and has
    # the authorization to edit/delete the item
    if 'username' in login_session and login_session['username'] == user.email:
        user_authorized = True
    else:
        user_authorized = False
    return render_template('itemDescription.html',
                           item=item,
                           category_name=category_name,
                           user_authorized=user_authorized)


# Create a new item
@app.route('/catalog/<category_name>/new', methods=['GET', 'POST'])
def add_item(category_name):
    """
        On GET, Render a form to add a new item to the catalog.
        On POST, save the new item to the database.
    """

    # Check if user is logged in to enable adding a new item
    if 'username' not in login_session:
        flash('You must be logged in to add a new item!')
        return redirect('/login')

    # Add new item
    if request.method == 'POST':
        user = get_user_info_by_emaild(login_session['username'])

        # Check which button was clicked, Add or Cancel
        # If Add/Submit button clicked, add the item to the database
        if 'submit' in request.form.keys() and request.form['submit'] == "Add":

            category_id = request.form['category']
            category = session.query(Category).filter_by(id=category_id).first()
            new_item = Item(title=request.form['title'], description=request.form['description'],
                            cat_id=category_id, category=category, user_id=user.id, user=user)
            session.add(new_item)
            session.commit()
            flash('New Item %s Successfully Created')

            # render a page that lists all the items of the newly added item's category
            return redirect(url_for('show_items_for_category', category_name=category.name, category_id=category_id))
        else:
            # render a page that lists all the items of the newly added item's category
            return redirect(url_for('show_latest_items'))
    else:
        # Serve add item form to client - GET request
        categories_list = session.query(Category).order_by(asc(Category.name)).all()

        # Check if category is already selected, else set default to Basketball
        if category_name is None:
            category_name = "Basketball"

        return render_template('addNewItem.html', categories_list=categories_list, selected_category=category_name)


@app.route('/catalog/<category_name>/<item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id, category_name):
    """
        On GET request, Render a form to edit the selected item.
        On POST request, save the edited item to the database.
    """

    # Check if user is logged in to enable editing of an item
    if 'username' not in login_session:
        flash('You must be logged in to edit an item!')
        return redirect('/login')

    # Edit item
    item_to_edit = session.query(Item).filter_by(id=item_id).first()
    if request.method == 'POST':
        # Check which button was clicked, Save or Cancel
        # If Save/Submit button clicked, save the edited item to the database
        if 'submit' in request.form.keys() and request.form['submit'] == "Save":
            user = get_user_info_by_emaild(login_session['username'])

            if request.form['title']:
                item_to_edit.title = request.form['title']
            if request.form['description']:
                item_to_edit.description = request.form['description']
            if request.form['category']:
                item_to_edit.cat_id = request.form['category']
            session.add(item_to_edit)
            session.commit()
            flash('Item Successfully Edited')

        # render a page that lists all the items of the edited item's category
        return redirect(url_for('show_items_for_category', category_name=category_name))
    else:
        # Check if user is logged in and also check if he owns the item and has
        # the authorization to edit/delete the item
        user = get_user_info_by_id(item_to_edit.user_id)
        if 'username' in login_session and login_session['username'] == user.email:
            # Serve edit item form to client - GET request
            categories_list = session.query(Category).order_by(asc(Category.id)).all()
            return render_template('editItem.html',
                                   categories_list=categories_list,
                                   item=item_to_edit)
        else:
            # not authorized to edit the item, return back to home page
            flash('Not authorized to edit item')
            return redirect(url_for('show_items_for_category', category_name=category_name))


@app.route('/catalog/<category_name>/<item_id>/delete', methods=['GET', 'POST'])
def delete_item(item_id, category_name):
    """
        On GET request, Render a form to delete the selected item.
        On POST request, delete the item from the database.
    """

    # Check if user is logged in to enable deleting of an item
    if 'username' not in login_session:
        flash('You must be logged in to delete an item!')
        return redirect('/login')
    item_to_delete = session.query(Item).filter_by(id=item_id).first()
    # Delete item
    if request.method == 'POST':
        # Check which button was clicked, Delete or Cancel
        # If Delete/Submit button clicked, delete the item from the database
        if 'submit' in request.form.keys() and request.form['submit'] == "Delete":
            user = get_user_info_by_emaild(login_session['username'])
            session.delete(item_to_delete)
            session.commit()
            flash('Item Successfully Deleted')

        # render a page that lists all the items of the deleted item's category
        return redirect(url_for('show_items_for_category', category_name=category_name))
    else:

        # Check if user is logged in and also check if he owns the item and has
        # the authorization to edit/delete the item
        user = get_user_info_by_id(item_to_delete.user_id)
        if 'username' in login_session and login_session['username'] == user.email:
            # Serve delete item form to client - GET request
            return render_template('deleteItem.html',
                                   item=item_to_delete)
        else:
            # not authorized to delete the item, return back to home page
            flash('Not authorized to delete item')
            return redirect(url_for('show_items_for_category', category_name=category_name))


@app.route('/json')
@app.route('/JSON')
def all_json():
    """
        Returns serialized JSON of joined dataset (all categories + items within them)
    """
    all_data = session.query(Category)
    return jsonify(categories=[category.serialize for category in all_data.all()])


# json endpoint for a list of all items
@app.route('/items/json')
@app.route('/items/JSON')
def items_json():
    items = session.query(Item).all()
    return jsonify(items=[i.serialize for i in items])


# json endpoint for a list of items for a category
@app.route('/catalog/<int:category_id>/items/JSON')
@app.route('/catalog/<int:category_id>/items/json')
def items_for_a_category_json(category_id):
    category = session.query(Category).filter_by(id=category_id).first()
    items = session.query(Item).filter_by(cat_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


# json endpoint for an item
@app.route('/catalog/<int:item_id>/JSON')
@app.route('/catalog/<int:item_id>/json')
def item_json(item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    return jsonify(item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
