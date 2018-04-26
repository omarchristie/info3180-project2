"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, filefolder, token_key
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegistrationForm, newPostForm
from models import Users, Posts, Likes, Follows
import os
import jwt
import datetime
from werkzeug.utils import secure_filename
from functools import wraps

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')
    
    
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            result = request.headers['Authorization'].split()
            token = result [1]

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, token_key)
            current_user = Users.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages


@app.route('/api/users/register',methods=["POST"])
def registerUser():
    
    #form = RegistrationForm()
    
    #if request.method == "POST" and form.validate_on_submit():
        # Data sent from the form that is requested
        # firstName = request.form['firstName']
        # lastName  = request.form['lastName']
        # userName  = request.form['userName']
        # password  = request.form['password']
        # email     = request.form['email']
        # location  = request.form['location']
        # biography = request.form['biography']
        # proPhoto  = request.files['proPhoto']
    data = request.get_json()
    #profile_picture = secure_filename(proPhoto.filename)
    now = datetime.datetime.now()
        #user = Users(firstName = firstName, lastName = lastName, userName = userName, password = password, email = email, location = location, biography = biography, proPhoto = profile_picture, joined_on = now )
    user = Users(firstName = data['firstname'], lastName = data['lastName'], userName = data['username'], password = data['password'], email = data['email'], location = data['location'], biography = data['biography'], proPhoto = data['profile_picture'], joined_on = now )
    db.session.add(user)
    db.session.commit()
    #proPhoto.save(os.path.join(filefolder, profile_picture))
        
    # register_body = [{"message": "User successfully registered"}]
    # return jsonify(result=register_body)
    # error_collection = form_errors(form)
    # error = [{'errors': error_collection}]
    # return  jsonify(errors=error)
    
@app.route('/api/auth/login', methods=["POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        userName = request.form['userName']
        password = request.form['password']
        
        user = Users.query.filter_by(userName=userName, password=password).first()
        token = jwt.encode({'user_id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, token_key)
        login_body = [{"message":  "User successfully logged in.", 'token' : token.decode('UTF-8')}]
        return jsonify(result=login_body)
    error_collection = form_errors(form)
    error = [{'errors': error_collection}]
    return  jsonify(errors=error)    

@app.route('/api/auth/logout', methods=["GET"])
@token_required
def logout(current_user):
    return ("noting")
 #KYZER WAS ERE DOING FUCKRY

@app.route('/api/posts',methods=["GET"])
def get_all_posts():
    # query database for all post
        #create dictionary
    # output list to hold dictionary
    output = []
    for post in posts:
        # create dictionary
        post_data = {}
        # add data from database to dictionary
        post_data['id'] = post.id
        post_data['userID'] = posts.userID
        post_data['photo'] = post.photo
        post_data['caption'] = post.caption
        post_data['created_on'] = post.created_on
        output.append(post_data)
    return jsonify({'posts': output})

@app.route('/api/users/{user_id}/posts',methods=["GET","POST"])
def make_post(user_id):
    
    form = newPostForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            user = Users.query.filter_by(user_id=user.id).first()
            description = request.form['description']
            photo  = request.files['photo']
            now = datetime.datetime.now()
            
            post_picture = secure_filename(photo.filename)
            post = Posts(userID = user, photo = post_picture, caption = description, created_on = now)
            
            db.session.add(post)
            db.session.commit(post)
            
            photo.save(os.path.join(filefolder, post_picture))
            post_body = [{"message": "Successfully created a new post"}]
            return jsonify(result=post_body)
            
    elif request.method == "GET":
        user_posts = Users.query.filter_by(user_id=user_id).all()
        if not user:
            return jsonify({'message': "no user found"})
        # output list to hold dictionary    
        output = []
        for user_post in user_posts:
            # create dictionary
            post_data = {}
            # add data from database to dictionary
            user_post['id'] = user_post.id
            user_post['userID'] = user_post.userID
            user_post['photo'] = user_post.photo
            user_post['caption'] = user_post.caption
            user_post['created_on'] = user_post.created_on
            output.append(post_data)
        return jsonify({'posts': output})
    error_collection = form_errors(form)
    error = [{'errors': error_collection}]
    return  jsonify(errors=error)
    
@app.route('/api/users/<user_id>/follow',methods=["POST"])
@token_required
def create_follow(current_user, user_id):
    user = Users.query.filter_by(user_id=user.id).first()
    if user is None:
        return jsonify ({'message': 'user not found'})
    if user == current_user:
        return jsonify ({'message': 'you cannot follow yourself'})
    followID = user_id
    userID = current_user.id
    follow = Follows(userID = userID, followerID = followID)
    db.session.add(follow)
    db.session.commit(follow)
    return jsonify ({'message': 'You followed a user'})
    
    
@app.route('/api/users/<post_id>/like',methods=["POST"])
@token_required
def create_like(current_user, post_id):
    userID = current_user.userID
    postID = post_id
    like = Likes(userID = userID, postID = postID)
    db.session.add(like)
    db.session.commit(like)
    return jsonify ({'message': 'You liked a user post'})
    
    
@app.route('/secure-page')

def secure_page():
    """Render a secure page on our website that only logged in users can access."""
    return render_template('secure_page.html')
    

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
