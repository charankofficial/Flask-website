# import mysql.connector
# cnx =None
# def get_sql_connect():
#     global cnx
#     if cnx is None:
#         cnx = mysql.connector.connect(user='root', password='root',
#                                 host='127.0.0.1',
#                                 database='db',port=3306)
#     return cnx

# def get_cursor():
#     connection = get_sql_connect()
#     return connection.cursor(buffered=True)
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file (only for local development)
load_dotenv()

# Get Firebase key contents from an environment variable
firebase_key_contents = os.getenv('FIREBASE_KEY_CONTENTS')

# Verify if the environment variable is properly set
if not firebase_key_contents:
    raise ValueError("The FIREBASE_KEY_CONTENTS environment variable is not set.")

# Convert the key contents (a JSON string) to a dictionary
try:
    firebase_key_dict = json.loads(firebase_key_contents)
except json.JSONDecodeError as e:
    raise ValueError("The FIREBASE_KEY_CONTENTS environment variable is not a valid JSON.") from e

# Use the service account key to connect to Firebase
cred = credentials.Certificate(firebase_key_dict)
firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

def get_firestore_client():
    """Returns the Firestore client instance."""
    return db

