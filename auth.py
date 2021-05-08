from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import *
from . import db

auth = Blueprint("auth", __name__)

@auth.route('register', methods = ['GET', 'POST'])
def Register():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if len(email) < 6:
            flash("Please Enter Valid Email!!", category="error")
        else:
            user = User.query.filter_by(email=email)
            if user:
                flash("Email Already Exists!!", category="error")
        if len(first_name) < 2:
            if len(first_name) == 0:
                flash("Please Enter First Name!!", category="error")
            else:
                flash("First Name Must Be Greater Than 4 Characters!!", category="error")
        elif len(last_name) < 2:
            if len(last_name) == 0:
                flash("Please Enter Last Name!!", category="error")
            else:
                flash("Last Name Must Be Greater Than 4 Characters!!", category="error")
        elif len(password) < 8:
            if len(password) == 0:
                flash("Please Enter Password!!", category="error")
            else:
                flash("Password Must Be Greater Than Or Equal To 8 Characters!!", category="error")

        elif password != confirm_password:
            flash("Password and Confirm Password Must Match!!", category="error")
        else:
            user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password, method='sha256'))
            db.session.add(user)
            db.session.commit()
            flash("Registered Successfully!!", category="success")
            return redirect(url_for('auth.Login'))
    return render_template("register.html", user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged In Successfully!!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.Home'))
            else:
                flash('Incorrect Password, Try Again.', category='error')
        else:
            flash('User Does Not Exist, Please Register Yourself!!', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def Logout():
    flash("Logged Out Successfully!!", category='success')
    logout_user()
    return redirect(url_for('auth.Login'))