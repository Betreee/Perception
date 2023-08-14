from datetime import datetime
import json
from app import  oauth, app
from flask import redirect, render_template, request, url_for, session
from .data import database, models
import os

# Get the absolute path to the directory where this script is located
dir_path = os.path.dirname(os.path.realpath("Perception"))
print(dir_path)
# Construct the absolute path to oauth.json
oauth_path = os.path.join("C:\\Users\\be\\OneDrive\\Documents\\GitHub\\Perception", '.secrets','oauth.json')

# Open the file
with open(oauth_path, 'r') as file:
    oauth_credentials = json.load(file)
    
google = oauth.remote_app(
    'google',
    consumer_key=oauth_credentials['web']['client_id'],
    consumer_secret=oauth_credentials['web']['client_secret'],
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/userinfo',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',)

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))
@app.route('/logout')
def logout():
    session.pop('google_token')
    return redirect(url_for('home'))  # Redirect to the home page or another appropriate page



@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo').data

    # Check if the user already exists in the database
    db_session = database.Session()
    user = db_session.query(models.User).filter_by(google_id=user_info['id']).first()

    # If the user doesn't exist, create a new user record
    if user is None:
        user = models.User(
            google_id=user_info['id'],
            email=user_info['email'],
            # Add any other fields you want to store
        )
        db_session.add(user)
        db_session.commit()

    # You can now log the user into your application, store the user's ID in the session, etc.
    session['user_id'] = user.id

    return redirect(url_for('profile_setup'))# Redirect to the home page or another appropriate page

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile_setup', methods=['GET', 'POST'])
def profile_setup():
   # Retrieve form data
    username = request.form['username']
    google_id = request.form['google_id']
    email = request.form['email']
    full_name = request.form['full_name']
    profile_picture = request.form['profile_picture']
    role = request.form['role']
    preferences = request.form['preferences'] # You may need to parse this from JSON
    date_joined = datetime.utcnow()
    last_login = datetime.utcnow() # You can update this value as needed
    status = request.form['status']
    bio = request.form['bio']
    location = request.form['location']

    # Save user data to the database
    user = models.User(
        username=username, 
        google_id=google_id,
        email=email, 
        full_name=full_name,
        profile_picture=profile_picture,
        role=role,
        preferences=preferences,
        date_joined=date_joined,
        last_login=last_login,
        status=status,
        bio=bio,
        location=location
    )
    session.add(user)
    session.commit()
    return render_template('profile_setup.html')