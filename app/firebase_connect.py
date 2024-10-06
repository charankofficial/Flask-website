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
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Firebase key path from an environment variable
firebase_key_path = os.getenv('FIREBASE_KEY_PATH')

# Verify if the environment variable is properly set
if not firebase_key_path:
    raise ValueError("The FIREBASE_KEY_PATH environment variable is not set.")
if not os.path.exists(firebase_key_path):
    raise ValueError(f"The FIREBASE_KEY_PATH is not valid: {firebase_key_path}")

# Use the service account key to connect to Firebase
cred = credentials.Certificate(firebase_key_path)
firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

def get_firestore_client():
    """Returns the Firestore client instance."""
    return db

