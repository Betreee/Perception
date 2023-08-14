import os
from flask import Flask
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Change this to a proper secret key
oauth = OAuth(app)

# Import OAuth-related routes
from app import oauth_setup, routes

