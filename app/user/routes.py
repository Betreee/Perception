import datetime
from flask import redirect, render_template, request, url_for
from sqlalchemy import JSON, Column, DateTime, Integer, String
from data.database import session
from data.models import User

from app import app
from flask import request, redirect, url_for, render_template
from data.database import session
from data.models import User


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
    user = User(
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