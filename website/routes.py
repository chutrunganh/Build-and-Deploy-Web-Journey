##############################################################################################################
# Define the routes/ URL paths for the website
# This file is responsible for the routes of the website
##############################################################################################################


from flask import Blueprint, render_template, request, flash 
# Use Blueprint to allow modulity, which means that routes can be defined in different files, not only in this file
# As in our case, we will have another file called auth.py that will contain the routes for the authentication steps
from flask_login import login_required, current_user # Import the login_user function
from .models import Note, db


routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST']) # Define the URL path for the home page (default page when you access the website)
@login_required # This decorator will ensure that this URL path can only be accessed by logged in users
def home():
    if request.method == 'POST': 
    # There are two forms in the home page, one for adding a note and the other for deleting a note
        # Handle note deletion
        if 'delete_note' in request.form:
            note_id = request.form.get('note_id')
            note = Note.query.get(note_id)
            if note and note.user_id == current_user.id:
                db.session.delete(note)
                db.session.commit()
                flash('Note deleted!', category='success')
            else:
                flash('Permission denied or note not found!', category='error')
        
        # Handle note creation
        else:
            note_content = request.form.get('note')
            if len(note_content.strip()) < 1:
                flash('Note cannot be empty!', category='error')
            else:
                new_note = Note(data=note_content, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added!', category='success')
    
    # Get all notes for current user
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, notes=notes)
