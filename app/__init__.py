# app/__init__.py
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Flask application instance
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configure MongoDB connection
client = MongoClient(os.getenv('MONGO_URI'))
db = client.healthcare_survey
