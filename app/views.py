"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""


import os
import jwt
from app import app, db, login_manager
from flask import request, jsonify, session, send_file, send_from_directory,render_template
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, RegistrationForm

from app.models import Users, Follows,Likes,Posts
from flask_wtf.csrf import generate_csrf
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

###
# Routing for your application.
###
@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.
    :param unicode user_id: user_id (email) user to retrieve
    """
    return Users.query.get(user_id)

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/register', methods = ['POST'])
def register():
    try:
        form = RegistrationForm()
        if request.method == "POST" and form.validate_on_submit():
            
            check_username = Users.query.filter_by(username=form.username.data).first()
            check_email = Users.query.filter_by(email=form.email.data).first()
            
            if check_username is not None or check_email is not None:
                return jsonify({
                    "errors": ["User is in the system"]
                }), 401


            username = form.username.data
            password = form.password.data
            firstname =  form.firstname.data
            lastname =  form.lastname.data
            email = form.email.data
            location = form.location.data
            biography = form.biography.data
            upload = form.profile_photo.data
            filename = secure_filename(upload.filename)
            joined_on = datetime.now()
            
            user = Users(username, password,firstname,lastname,email, location, biography, filename,joined_on)
            db.session.add(user)
            db.session.commit()
            upload.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            return jsonify({
                'message': "User Added Sucessfully",
                'id': user.id,
                'username': username,
                'firstname': firstname,
                'lastname': lastname,
                'photo': filename,
                'email': email,
                'location': location,
                'biography': biography,
                'joined_on': user.joined_on
            }), 201
        return jsonify(errors=form_errors(form)), 401
    except:
        return jsonify({ "errors": form.errors}), 500



@app.route("/api/v1/auth/login", methods=["POST"])
def login():
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        # Get the username and password values from the form.
        username = form.username.data
        password = form.password.data

        # This queries database for a user based on the username
        # and password submitted.
        user = Users.query.filter_by(username=username).first()

        # Compares the submited password and username to the hash password and
        # username in the database.
        if user is not None and check_password_hash(user.password, password):
            session['logged_in'] = True

            #Creates the token for the user currently logging in
            payload = {
                'sub': user.id, # subject, usually a unique identifier
                'user': username,
                'iat': datetime.utcnow(),# issued at time
                'exp': datetime.utcnow() + timedelta(hours=2) # expiration time
            }

            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            login_user(user)

            return jsonify(
                { 
                    "token": token , 
                    "message": "Login Successfully",
                    "id": user.id
                }), 200
        return jsonify(
                { 
                    "errors": ['Invalid credentials']
                }), 401
    
    return jsonify(errors=form_errors(form)), 401

@app.route('/api/v1/auth/logout', methods=["POST"])
@login_required

def logout():
    logout_user()

    return jsonify({
        "message": "Log out successful"
    }), 200

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

"""
    ROUTE to retrieve images from upload folder
"""
@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
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

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404