from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import *
from . import db

views = Blueprint("views", __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def Home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash("Note is Too Short!!", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note Added Successfully!!", category='success')
    return render_template("index.html", user=current_user)

@views.route('/delete-note/<int:id>', methods=['GET', 'POST'])
@login_required
def DeleteNote(id):
    if request.method == 'POST':
        note = Note.query.filter_by(id=id)
        note.delete()
        db.session.commit()
    return redirect(url_for('views.Home'))
