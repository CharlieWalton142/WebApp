from flask import Blueprint, render_template, request, flash, redirect, url_for
from .userModel import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__)


@auth.route('/login', methods = ['Get', 'Post'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        #filter all users that have this email
        # check against the inputted credentials
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in', category='sucess')
                login_user(user, remember= True)
                #remember the logged in user unless the webserver restarts
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    #login_user(remember=False)
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods = ['Get', 'Post'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        admin = 0
        #gets the data the user has inputted
        #checks if the email inputted already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email)< 4:
            flash('Email must be greater than 3 characters', category = 'error')
        elif len(first_name) < 2:
            flash('First Name must be greater than 1 characters', category = 'error')
        elif password1 != password2:
            flash('Passwords don\'t match', category = 'error')
        elif len(password1) < 8:
            flash('password must be greater than 7 characters', category = 'error')
        else:
            #add user
            new_user = User(email=email, first_name=first_name,admin = admin, password= generate_password_hash(password1, method="pbkdf2:sha256", salt_length=8))
            db.session.add(new_user)
            db.session.commit()
            #validation for creating the account
            login_user(new_user, remember=True)
            flash('Account created', category = 'success')
            #redirect to the home page
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)