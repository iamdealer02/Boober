from flask import Blueprint, render_template, redirect, url_for,flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

from Class.authentication.classes import RegistrationForm, LoginForm, User
from Database.SQL.client import add_user, check_user
from logger.log import auth_logger, time_logger
import time

authentication_bp = Blueprint("authentication", __name__, template_folder="templates")

bcrypt = Bcrypt()

@authentication_bp.route("/register/verify")
def verify():
    return render_template('verify.html')


@authentication_bp.route("/login", methods=['GET', 'POST'])
def login():
    start_time = time.time()
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = check_user(email)
        role = user[3]
        if user and bcrypt.check_password_hash(user[2], password):
            login_user(User(user[0], user[1], user[2]))
            print('LOGGED IN')
            flash('Login successful!', 'success')  # Flash a success message
            auth_logger.info(f'User {email} Logged in')
            end_time = time.time()
            time_logger.info(f'Login time: {end_time - start_time}')
            return redirect(url_for(f'{role}.{role}'))
        else:
            print('wrong credentials')
            auth_logger.info('User {email} Login failed')
            flash('Invalid email or password', 'error')  # Flash an error message

    return render_template('login.html', form=form)

@authentication_bp.route("/logout", methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    auth_logger.info('User Logged out')
    return redirect(url_for('home.home'))
