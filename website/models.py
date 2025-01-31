########################################################################
# This file contains the database models for the website. 
# Each class in this file represents a table in the database
########################################################################

from . import db # Import the database object from the __init__.py file
from flask_login import UserMixin
# UserMixin is a class that contains the default implementations for the methods that Flask-Login expects user objects to have
# aka, we use this class to ensure compatibility with Flask-Login depencies
from sqlalchemy.sql import func

# Each object in the database must first inherit from the db.Model class
class User(db.Model, UserMixin): # Multiple inheritance 
    id = db.Column(db.Integer, primary_key=True) # Define the columns of the table
    email = db.Column(db.String(150), unique=True) # Max length of 150 characters
    user_name = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    notes = db.relationship('Note') # Base on the foreign key in the Note table, we 
    # can get all the notes that a user has created


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date_created = db.Column(db.DateTime(timezone=True), default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Define the foreign key to the user table
    # This will create a relationship between the Note and User tables
    # This means that the Note table will have a column called user_id that will be a foreign key to the id column in the User table
    # This will allow us to get the user that created the note