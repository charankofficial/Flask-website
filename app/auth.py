from flask import Blueprint, render_template, request, redirect, url_for, flash
import bcrypt
from .sqlconnect import get_sql_connect,get_cursor
auth = Blueprint('auth', __name__, template_folder='../templates')
connect = get_sql_connect()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if request.method == 'POST':
    #     email = request.form.get('email')
    #     password = request.form.get('password')

    #     user = User.query.filter_by(email=email).first()

    #     if user and check_password_hash(user.password, password):
    #         flash('Logged in successfully!', category='success')
    #         return redirect(url_for('views.home'))
    #     else:
    #         flash('Login failed. Check your credentials.', category='error')

    return render_template('login.html')
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user already exists
        cursor = get_cursor()
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email address already exists.', category='error')
        else:
            # Insert new user into the database
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            query = ("INSERT INTO users "
                     "(email, password)"
                     "VALUES (%s, %s)")
            data = (email, hashed_password)
          
            cursor.execute(query,data)
            get_sql_connect().commit()  # Commit changes to the database
            flash('Account created successfully!', category='success')
            return redirect(url_for('auth.login'))

    return render_template('signup.html')