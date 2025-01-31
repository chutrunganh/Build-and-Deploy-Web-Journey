######################################################################################
# Initialize the Flask application and load all necessary modules     
######################################################################################
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager # Manage the login process

# Initialize the database
# The SQLAlchemy acts as intermediate between the database and the application
# It converts the tables in the database to Python objects, abstract the syntax of SQL queries
# SQLAlchemy can work with different databases, such as SQLite (default), MySQL, PostgreSQL, etc. 
db = SQLAlchemy()
DB_NAME = 'database.db' 

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test' # Use to encrypt session data

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # SQLite database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable the modification tracker
    db.init_app(app)

    # Create database if it doesn't exist
    from website.models import User, Note
    try:
        if not os.path.exists('website/' + DB_NAME):
            with app.app_context():
                db.create_all()
                print('Created database!')
    except Exception as e:
        print(f'Error creating database: {e}')

    
    # Import the routes from the routes.py file
    from website.routes import routes
    app.register_blueprint(routes) # Register the routes to the app

    # Import the routes from the auth.py file
    from website.auths import auths
    app.register_blueprint(auths) # Register the routes to the app

    # Initialize the login manager
    login_manager = LoginManager() 
    # When a user tries to access our page without being logged in, they
    # will be redirected to the login page and a message will be displayed
    login_manager.login_view = 'auths.login' 
    login_manager.login_message = "Please login to access this page"
    login_manager.login_message_category = "error" 
    login_manager.init_app(app)

    # Tell Flask how to load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


   
    
    return app