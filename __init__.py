#!/usr/bin/env python3
import os
from flask import Flask, render_template, request, redirect
from flask import url_for, jsonify, make_response, send_from_directory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from sqlalchemy.pool import SingletonThreadPool
from flask import session as login_session
import random
import string
import json
import httplib2
import requests
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from werkzeug.utils import secure_filename


path = os.path.dirname(__file__)

UPLOAD_FOLDER = (path+'./photo')
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CLIENT_ID = json.loads(open('/var/www/FlaskApp/FlaskApp/readBook/client_secrets.json',
                            'r').read())['web']['client_id']



# Instance, every time it runs create instance name

#SQLALCHEMY_DATABASE_URI =  'sqlite://' + os.path.join(basedir, 'catalog.db')

engine = create_engine(
    'sqlite:////var/www/FlaskApp/FlaskApp/readBook/catalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token


@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(path+'/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

# Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

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
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    if 'name' in data:
        login_session['username'] = data['name']
    else:
        login_session['username'] = "NAN"

    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['id'] = data['id']

    # see if user exists, if it does't make a new one

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    print("done!")

    return ("username : " + login_session['username'] + " , email : " +
            login_session['email'])


# User Helper Functions

def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = ('https://accounts.google.com/o/oauth2/'
           'revoke?token=%s' % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        login_session.clear()
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('showAllCategory'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Category Items


@app.route('/catalog/<category_name>/JSON')
def catalogJSON(category_name):
    categoryId = session.query(Category).filter_by(
        name=category_name).first().id
    CategoryItems = session.query(CategoryItem).filter_by(
        categoryId=categoryId).all()
    return jsonify(Category=[i.serialize for i in CategoryItems])


# Main Route Show all  Category


@app.route('/')
@app.route('/catalog')
def showAllCategory():
    if 'email' in login_session:
        userId = getUserID(login_session['email'])
        if userId:
            userInfo = getUserInfo(userId)
    else:
        userInfo = None
        userId = None
    CategoryItems = session.query(CategoryItem).all()
    return render_template(
        'index.html',
        user_loged_in='username' in login_session,
        list=CategoryItems,
        userInfo=userInfo)


#  Show all Items for Specific category


@app.route('/catalog/<category_name>')
def showCategoryItems(category_name):
    if 'email' in login_session:
        userId = getUserID(login_session['email'])
        if userId:
            userInfo = getUserInfo(userId)
    else:
        userInfo = None
        userId = None
    categoryId = session.query(Category).filter_by(
        name=category_name).first().id
    CategoryItems = session.query(CategoryItem).filter_by(
        categoryId=categoryId).all()
    return render_template(
        'index.html',
        user_loged_in='username' in login_session,
        list=CategoryItems,
        userInfo=userInfo)


# Show one Specific Item


@app.route('/catalog/<category_name>/<item_title>')
def showCategoryItem(category_name, item_title):
    if 'email' in login_session:
        userId = getUserID(login_session['email'])
        print()
        if userId:
            userInfo = getUserInfo(userId)
    else:
        userInfo = None
        userId = None
    item = session.query(CategoryItem).filter_by(title=item_title).one()
    return render_template(
        'Item.html',
        user_loged_in='username' in login_session,
        item=item,
        userInfo=userInfo,
        user_id=userId)


# Save File Functions

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# save a file and return the path


def save_file(file, Title, Author):
    picture = "/photo/book.png"
    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
        return picture

    # if user does not select file, browser also
    if file.filename == '':
        print('No selected file')
        return picture
    # save file , and return the path
    if file and allowed_file(file.filename):
        print(file.filename)
        print(allowed_file(file.filename))
        filename = Title + "_" + Author + ".png"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("saved" + " url = " + filename)
        picture = "/photo/"+filename
        return picture

    print("file not allowed")
    return picture

# Create a new Item


@app.route('/catalog/new', methods=['GET', 'POST'])
def newCategoryItem():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if (request.form['Title'] and request.form['Author']
                and request.form['Description']):
            categoryId = session.query(Category).filter_by(
                name=request.form.get('category')).first().id
            picture = save_file(request.files['file'],
                                request.form['Title'], request.form['Author'])
            newItem = CategoryItem(
                title=request.form['Title'],
                description=request.form['Description'],
                categoryId=categoryId,
                user_id=login_session['user_id'],
                author=request.form['Author'],
                picture=picture)
            session.add(newItem)
            session.commit()
            return redirect(
                url_for(
                    'showCategoryItems',
                    category_name=request.form.get('category')))
        return redirect(url_for('showAllCategory'))
    else:
        if 'email' in login_session:
            userId = getUserID(login_session['email'])
            if userId:
                userInfo = getUserInfo(userId)
        else:
            userInfo = None
            userId = None
        return render_template('newItemPage.html', user_loged_in='username' in
                               login_session, userInfo=userInfo)


# Edit an Item


@app.route('/catalog/<item_title>/edit', methods=['GET', 'POST'])
def editCategoryItem(item_title):

    if 'username' not in login_session:
        return redirect('/login')

    Item = session.query(CategoryItem).filter_by(title=item_title).one()
    if Item.user_id != login_session['user_id']:
        html = '''<script> function myfunction()
            {alert('You are not authorized to edit this Item.');}
            </script><body onload='myfunction()''>'''
        return html

    if request.method == 'POST':
        categoryId = session.query(Category).filter_by(
            name=request.form.get('category')).first().id
        if request.form['Title']:
            Item.title = request.form['Title']
        if request.form['Author']:
            Item.author = request.form['Author']
        if request.form['Description']:
            Item.description = request.form['Description']
        Item.categoryId = categoryId
        if 'file' in request.files:
            if request.files['file'].filename != '':
                print("file >> "+request.files['file'].filename)
                picture = save_file(
                    request.files['file'], request.form['Title'],
                    request.form['Author'])
                Item.picture = picture
        session.add(Item)
        session.commit()
        return redirect(
            url_for('showCategoryItems', category_name=Item.category.name))

    else:
        if 'email' in login_session:
            userId = getUserID(login_session['email'])
            if userId:
                userInfo = getUserInfo(userId)
        else:
            userInfo = None
            userId = None
        return render_template(
            'editPage.html', item=Item,
            user_loged_in='username' in login_session, userInfo=userInfo)


# Delete an Item


@app.route('/catalog/<item_title>/delete')
def deleteCategoryItem(item_title):
    if 'username' not in login_session:
        return redirect('/login')
    Item = session.query(CategoryItem).filter_by(title=item_title).one()
    if Item.user_id != login_session['user_id']:
        html = '''<script> function myfunction()
            {alert('You are not authorized to delete this Item.');}
            </script><body onload='myfunction()''>'''
        return html
    category_name = Item.category.name

    session.delete(Item)
    session.commit()
    return redirect(
        url_for('showCategoryItems', category_name=category_name))


# return photo endpoint

@app.route('/photo/<filename>')
def photo(filename):
    return send_from_directory("./photo", filename)


# Main part runs if there is no exceptions, from python interpretur
if __name__ == '__main__':
    app.secret_key = '''\xe5\xd7\xe3\x90|d\x99\xf96\xd9\xe7\
        xe6I\x02\xf6\xe5\x03z\x84\x90\x94\x15n\x99'''
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
