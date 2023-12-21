from flask import Blueprint, render_template, redirect,request, jsonify, session
from flask_login import login_required, current_user
from Class.authentication.classes import RegistrationForm
from flask_bcrypt import Bcrypt
from Database.SQL.client import add_user
from Database.MongoDB.rides import add_rides, get_otp, add_otp,get_driver_id, get_ride_details
from Database.MongoDB.driver import get_driver_details
from Helpers.OTP.otp import generate_hotp, generate_random_secret_key, hash_otp, verify_otp

client_bp = Blueprint("client", __name__, template_folder="templates")
bcrypt = Bcrypt()

@client_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print('registering')
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        role = 'client'
        add_user(email, hashed_password, role)
            
    return render_template('clientregister.html', form=form)


@client_bp.route("/")
@login_required
def client():
    if current_user.role == 'client':
        return render_template('client.html')

@client_bp.route("/ride", methods=['POST'])
@login_required
def handle_ride_data():
    if current_user.role == 'client':
        data = request.get_json()
        print(data)
        ride_id = add_rides(current_user.id, data.get('pickup'), data.get('dropoff'))
        print(ride_id)
        return jsonify({'ride_id': str(ride_id)})


@client_bp.route("/ride/<ride_id>", methods=['GET'])
@login_required
def client_ride(ride_id):
    # Needs : OTP generated, driver assigned details
    # generating the OTPs and hashing it and saving it in the database
    # generating random secret_key everytimes
    
    if current_user.role == 'client':

        driver_id = get_driver_id(ride_id)
        driver_details = get_driver_details(driver_id)
        ride_data = get_ride_details(ride_id)
        # get_otp gets the hashed otp from the database and display the otp to client
        otp = get_otp(ride_id)
        if otp == None:
            secret_key = generate_random_secret_key()
            otp = generate_hotp(secret_key)
            session['otp'] = otp
            # hash otp and add otp to the database
            hashed_otp = hash_otp(otp)
            print(hashed_otp)
            add_otp(ride_id,hashed_otp)
        return render_template('clientRide.html', otp=session['otp'], driver_details = driver_details, ride_data=ride_data)