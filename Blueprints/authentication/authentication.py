from flask import Blueprint, render_template, redirect, url_for,flash, g
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

from Class.authentication.classes import RegistrationForm, LoginForm, User
from Database.SQL.client import add_user, check_user

authentication_bp = Blueprint("authentication", __name__, template_folder="templates")

bcrypt = Bcrypt()

@authentication_bp.route("/register/verify")
def verify():
    return render_template('verify.html')


@authentication_bp.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        g.user_email = email
        user = check_user(email)
        role = user[3]
        if user and bcrypt.check_password_hash(user[2], password):
            login_user(User(user[0], user[1], user[2]))
            print('LOGGED IN')
            flash('Login successful!', 'success')  # Flash a success message
         
            return redirect(url_for(f'{role}.{role}'))
        else:
            print('wrong credentials')
       
            flash('Invalid email or password', 'error')  # Flash an error message

    return render_template('login.html', form=form)

@authentication_bp.route("/logout", methods=['POST','GET'])
@login_required
def logout():
    user_email = g.pop('user_email', 'Unknown')
    logout_user()
  
    return redirect(url_for('home.home'))
