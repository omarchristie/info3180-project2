"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, filefolder, token_key
from flask import render_template, request, redirect, url_for, flash, jsonify, g, session
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
    
    
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None)
    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
         payload = jwt.decode(token, token_key)
         get_user = Users.query.filter_by(id=payload['user_id']).first()

    except jwt.ExpiredSignature:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = get_user
    return f(*args, **kwargs)

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

@app.route('/')
def index():
    form1 = RegistrationForm()
    """Render website's initial page and let VueJS take over."""
    return render_template('index.html', form1=form1)
    
    
@app.route('/api/users/register',methods=["POST"])
def registerUser():
    form = RegistrationForm()
    
    if request.method == "POST" and form.validate_on_submit():
        #Data sent from the form that is requested
        userName  = request.form['userName']
        password  = request.form['password']
        firstName = request.form['firstName']
        lastName  = request.form['lastName']
        email     = request.form['email']
        location  = request.form['location']
        biography = request.form['biography']
        proPhoto  = request.files['proPhoto']
        profile_picture = secure_filename(proPhoto.filename)
        now = datetime.datetime.now()
        user = Users(firstname = firstName, lastname = lastName, username = userName, password = password, email = email, location = location, biography = biography, proPhoto = profile_picture, joined_on = now )
        db.session.add(user)
        db.session.commit()
        proPhoto.save(os.path.join(filefolder, profile_picture))
        register_body = [{"message": "User successfully registered"}]
        return jsonify(result=register_body)
    error_collection = form_errors(form)
    error = [{'errors': error_collection}]
    return  jsonify(errors=error)
    
@app.route('/api/auth/login', methods=["POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        userName = request.form['userName']
        password = request.form['password']
        
        user = Users.query.filter_by(username=userName, password=password).first()
        payload = {'user_id' : user.id}
        token = jwt.encode(payload, token_key)
        session['userid'] = user.id;
        return jsonify(data={'token': token, 'userid': user.id}, message="User logged in")
    error_collection = form_errors(form)
    error = [{'errors': error_collection}]
    return  jsonify(errors=error)    

@app.route('/api/auth/logout', methods=["GET"])
@requires_auth
def logout():
    g.current_user = None
    session.pop('userid', None)
    return jsonify(message = "logout")
 
@app.route('/test/', methods=["GET", "POST"])
def test():
    numberfollow = Follows.query.filter_by(userID=13)
    numberoffollower=[]
    for number in numberfollow:
        numberoffollower.append(number)
    return render_template("test.html", post=numberoffollower.length())

@app.route('/api/posts/', methods=["GET"])
@requires_auth
def get_all_posts():
    # query database for all post
    posts = Posts.query.order_by(Posts.created_on.desc()).all()
    # output list to hold dictionary
    output = []
    for post in posts:
        user = Users.query.filter_by(id = post.userID).first()
        numberlikes = Likes.query.filter_by(postID = post.id).all()
        numberoflikes=[];
        for number in numberlikes:
            num = {'test': "counted"}
            numberoflikes.append(num)
        postdate= post.created_on.strftime("%d %b %Y");
        posted= {"postid":post.id,"userid": post.userID, "username": user.username, "pro_photo": user.proPhoto, "photo": post.photo, "caption": post.caption, "created_on": postdate, "likes": numberoflikes}
        output.append(posted)
    return jsonify(data= output)

@app.route('/api/users/<user_id>/posts',methods=["GET","POST"])
@requires_auth
def make_post(user_id):
    form = newPostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            userID = user_id
            caption = request.form['caption']
            photo  = request.files['photo']
            now = datetime.datetime.now()
            
            post_picture = secure_filename(photo.filename)
            post = Posts(userID = userID, photo = post_picture, caption = caption, created_on = now)
            
            db.session.add(post)
            db.session.commit()
            
            photo.save(os.path.join(filefolder, post_picture))
            return jsonify({'message':"Successfully created a new post"})
            
    elif request.method == "GET":
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'message': "no user found"})
        user_posts = Posts.query.filter_by(userID=user_id).all()
        # output list to hold dictionary    
        output = []
        for user_post in user_posts:
            # create dictionary
            post_data = {'id':user_post.id,'userID': user_post.userID,'photo': user_post.photo,'caption': user_post.caption,'created_on': user_post.created_on}
            output.append(post_data)
        return jsonify(data=output)
    error_collection = form_errors(form)
    error = [{'errors': error_collection}]
    return  jsonify(errors=error)
    
    
@app.route('/api/users/<user_id>/', methods=["GET"])
@requires_auth
def get_user(user_id):
    # query database for all post
    user = Users.query.filter_by(id=user_id).first()
    output = []
    # output list to hold dictionary
    if (int(user_id) == session['userid']):
        join= user.joined_on.strftime("%B %Y");
        info= {"userid": user.id, "username": user.username, "firstname": user.firstname, "lastname": user.lastname, "email": user.email, "location": user.location, "biography": user.biography,"photo": user.proPhoto, "joined_on": join}
        output.append(info)
        return jsonify(profile = output, isuser=True)
    join= user.joined_on.strftime("%B %Y");
    info= {"userid": user.id, "username": user.username, "firstname": user.firstname, "lastname": user.lastname, "email": user.email, "location": user.location, "biography": user.biography,"photo": user.proPhoto, "joined_on": join}
    output.append(info)
    return jsonify(profile= output)
    
@app.route('/api/users/<user_id>/followersnumber',methods=["GET"])
@requires_auth
def followersnumber(user_id):
    numberfollow = Follows.query.filter_by(userID=user_id).all()
    numberoffollower=[]
    for number in numberfollow:
        num = {'test': "counted"}
        numberoffollower.append(num)
    return jsonify (follower= numberoffollower)
    
@app.route('/api/users/<user_id>/following',methods=["GET"])
@requires_auth
def followercheck(user_id):
    followcheck = Follows.query.filter_by(userID=user_id, followerID=session['userid']).first()
    if(followcheck is None):
        return jsonify (following= False)
    return jsonify (following= True)
    
@app.route('/api/users/<user_id>/follow',methods=["POST"])
@requires_auth
def create_follow(user_id):
    follow = Follows(userID = user_id, followerID = session['userid'])
    db.session.add(follow)
    db.session.commit()
    return jsonify (message= 'You followed a user')
    
    
@app.route('/api/users/<post_id>/like',methods=["POST"])
@requires_auth
def create_like(post_id):
    likecheck = Likes.query.filter_by(userID=session['userid'], postID=post_id).first()
    if(likecheck is None):
        like = Likes(userID = session['userid'], postID = post_id)
        db.session.add(like)
        db.session.commit()
        return jsonify (message= 'You like a post')
    return jsonify (DB= 'Already liked post')
    


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
