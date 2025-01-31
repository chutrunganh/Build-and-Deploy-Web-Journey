##############################################################################################################
# Define the routes/ URL paths for the website, only for the authentication steps (This can be considers 
# as extension for the main routes.py)
##############################################################################################################

from flask import Blueprint, render_template, request, flash, redirect, url_for
# Use Blueprint to allow modulity, which means that routes can be defined in different files, not only in this file
# As in our case, we will have another file called auth.py that will contain the routes for the authentication steps
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user # Import the login_user function

auths = Blueprint('auths', __name__)

@auths.route('/login',methods=['GET', 'POST']) # Login page
def login():
    if request.method == 'POST':
        # If the form is empty, refresh the page the page will be considered as GET request
        # So, the code will not be executed
        user_name = request.form.get('username')
        password = request.form.get('password')
        # Check if the user exists
        user = User.query.filter_by(user_name=user_name).first()
        login_user(user, remember=True) # Remember the user until the browser session/ cookie is closed or our webserver is restarted
        if user:
            # Check if the password is correct
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # If login successfull, redirect to the home page and also pass the user object
                return redirect(url_for('routes.home',user=current_user)) 
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')
    return render_template("login.html", user=current_user)

@auths.route('/register', methods=['GET', 'POST']) # Register page
# We need to defind the methods that the route will accept (GET is always accepted by default). POST is used to send data to the server
def register():
    if request.method == 'POST': # If the form is submitted
        # If the form is empty, refresh the page the page will be considered as GET request
        # So, the code will not be executed
        email = request.form.get('email')
        user_name = request.form.get('username')
        password = request.form.get('password')
        confirm_password2 = request.form.get('confirm_password')

        if len(user_name) < 4: # Flash a message to the screen
            flash('Username must be greater than 4 characters.', category='error')
        if password != confirm_password2:
            flash('Passwords don\'t match.', category='error')
        else:
            flash('Account created!', category='success')
            # Add the user to the database
            # Check if email already exists
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', category='error')
                return render_template("register.html")
            # Check if username already exists
            user = User.query.filter_by(user_name=user_name).first()
            if user:
                flash('Username already exists.', category='error')
                return render_template("register.html")
            
            user = User(email=email, user_name=user_name, password=generate_password_hash(password, method='pbkdf2:sha1'))
            db.session.add(user)
            db.session.commit()
            # After user register, sign in the user
            login_user(user, remember=True)
            # Redirect to the home page
            return redirect(url_for('routes.home',user=current_user))
        
    return render_template("register.html", user=current_user)



@auths.route('/logout') # Logout page
@login_required # Ensure that this URL path can only be accessed by logged in users
def logout():
   # Redirect to the login page
    logout_user()
    return redirect(url_for('auths.login'))