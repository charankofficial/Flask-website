# from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# import bcrypt
# from .sqlconnect import get_sql_connect, get_cursor

# auth = Blueprint('auth', __name__, template_folder='../templates')

# @auth.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         cursor = get_cursor()
#         cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
#         existing_user = cursor.fetchone()

#         if existing_user:
#             flash('Email address already exists.', category='error')
#         else:
#             hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#             query = "INSERT INTO users (email, password) VALUES (%s, %s)"
#             data = (email, hashed_password.decode('utf-8'))
#             cursor.execute(query, data)

#             connect = get_sql_connect()
#             connect.commit()

#             flash('Account created successfully!', category='success')
#             return redirect(url_for('auth.login'))

#     return render_template('signup.html')


# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         cursor = get_cursor()
#         cursor.execute("SELECT email, password FROM users WHERE email = %s", (email,))
#         user = cursor.fetchone()

#         if user:
#             stored_hashed_password = user[1]

#             if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
#                 session['user'] = email  
#                 return render_template('mypage.html')  
#             else:
#                 flash('Incorrect password. Please try again.', category='error')
#         else:
#             flash('Email not found. Please sign up first.', category='error')

#     return render_template('login.html')


# @auth.route('/logout')
# def logout():
#     session.pop('user', None)
#     flash('You have been logged out.', category='success')
#     return redirect(url_for('auth.login'))

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import bcrypt
from .firebase_connect import get_firestore_client

# Create the blueprint for auth
auth = Blueprint('auth', __name__, template_folder='../templates')

# Get Firestore client
db = get_firestore_client()

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the email and password from the form
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user already exists
        users_ref = db.collection('users')
        existing_user_query = users_ref.where('email', '==', email).get()

        if existing_user_query:
            flash('Email address already exists.', category='error')
        else:
            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Create new user document in Firestore
            new_user = {
                'email': email,
                'password': hashed_password
            }
            users_ref.add(new_user)

            flash('Account created successfully!', category='success')
            return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the email and password from the form
        email = request.form.get('email')
        password = request.form.get('password')

        # Query to find the user by email
        users_ref = db.collection('users')
        existing_user_query = users_ref.where('email', '==', email).get()

        if existing_user_query:
            user = existing_user_query[0].to_dict()
            stored_hashed_password = user['password']

            # Verify the provided password with the stored hash
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                # Passwords match
                session['user'] = email  # Store user in session
                return render_template('mypage.html')  # Render mypage.html upon successful login
            else:
                # Passwords don't match
                flash('Incorrect password. Please try again.', category='error')
        else:
            # No user found
            flash('Email not found. Please sign up first.', category='error')

    return render_template('login.html')

@auth.route('/logout')
def logout():
    # Clear the session data to log out the user
    session.pop('user', None)
    flash('You have been logged out.', category='success')
    return redirect(url_for('auth.login'))
