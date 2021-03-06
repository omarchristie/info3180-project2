"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm
from models import UserProfile

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
@app.route('/api/users/register',methods=["POST"])
def registerUser():
    
    form = RegistrationForm()
    
    if request.method == "POST" and form.validate_on_submit():
        # Data sent from the form that is requested
        firstName = request.form['firstName']
        lastName  = request.form['lastName']
        userName  = request.form['userName']
        password  = request.form['password']
        email     = request.form['email']
        location  = request.form['location']
        biography = request.form['biography']
        
        proPhoto  = request.files['proPhoto']
        profile_picture = secure_filename(proPhoto.filename)
        proPhoto.save(os.path.join(filefolder, profile_picture))
        
        register_body = [{"message": "User successfully registered", "firstname": firstName,"lastname": lastName,"username": userName,
                           "password": password,"email": email,"location": location,"biography": biography,"profile_photo": proPhoto}]
        return jsonify(result=register_body)
    error_collection = form_errors(form)
    error = [{'errors': error_collection}]
    return  jsonify(errors=error)
    
@app.route('/api/auth/login')
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        userName = request.form['userName']
        password = request.form['password']
        
        login_body = [{"message":  "User successfully logged in."}]
        return jsonify(result=login_body)
    error_collection = form_errors(form)
    error = [{'errors': error_collection}]
    return  jsonify(errors=error)    
        
        
        
@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        # change this to actually validate the entire form submission
        # and not just one field
        username = form.username.data
        password = form.password.data
        user = UserProfile.query.filter_by(username=username, password=password).first()
        if user is not None:
            # Get the username and password values from the form.

            # using your model, query database for a user based on the username
            # and password submitted
            # store the result of that query to a `user` variable so it can be
            # passed to the login_user() method.
            remember_me = False
            if 'remember_me' in request.form:
                remember_me = True
            # get user id, load into session
            login_user(user, remember=remember_me)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')

            # remember to flash a message to the user
            return redirect(next_page or url_for('secure_page'))  # they should be redirected to a secure-page route instead
        else:
            flash('Username or Password is incorrect.', 'danger')
    return render_template("login.html", form=form)


@app.route('/secure-page')

def secure_page():
    """Render a secure page on our website that only logged in users can access."""
    return render_template('secure_page.html')
    
@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))    

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
