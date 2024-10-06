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
load_dotenv()
firebase_key_contents = os.getenv('FIREBASE_KEY_CONTENTS')
if not firebase_key_contents:
    raise ValueError("The FIREBASE_KEY_CONTENTS environment variable is not set.")
try:
    firebase_key_dict = json.loads(firebase_key_contents)
except json.JSONDecodeError as e:
    raise ValueError("The FIREBASE_KEY_CONTENTS environment variable is not a valid JSON.") from e

cred = credentials.Certificate(firebase_key_dict)
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_firestore_client():
    """Returns the Firestore client instance."""
    return db

