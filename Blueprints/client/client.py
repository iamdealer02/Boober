from flask import Blueprint, render_template, redirect,request, jsonify, session,url_for
from flask_login import login_required, current_user
from Class.authentication.classes import RegistrationForm
from flask_bcrypt import Bcrypt
from Database.SQL.client import add_user
from Database.MongoDB.rides import add_rides, get_otp, add_otp,get_driver_id, get_ride_details, get_all_previous_rides
from Database.MongoDB.driver import get_driver_details
from Helpers.OTP.otp import generate_hotp, generate_random_secret_key, hash_otp, verify_otp
from Database.MongoDB.client import add_client_address, add_client_email, add_client_name, get_client_info
import time
from logger.log import time_logger

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
        start_time = time.time()
        data = request.get_json()
        print(data)
        ride_id = add_rides(current_user.id, data.get('pickup'), data.get('dropoff'), data.get('ridePrice'))
        print(ride_id)
        end_time = time.time()
        elapsed_time = end_time - start_time
        time_logger.info(f'Route: /ride, Time: {elapsed_time}')
        return jsonify({'ride_id': str(ride_id)})


@client_bp.route("/ride/<ride_id>", methods=['GET'])
@login_required
def client_ride(ride_id):
    # Needs : OTP generated, driver assigned details
    # generating the OTPs and hashing it and saving it in the database
    # generating random secret_key everytimes
    
    if current_user.role == 'client':
        start_time = time.time()
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
        end_time = time.time()
        elapsed_time = end_time - start_time
        time_logger.info(f'Route: /ride/{ride_id}, Time: {elapsed_time}')
        return render_template('clientRide.html', otp=session['otp'], driver_details = driver_details, ride_data=ride_data)
    

@client_bp.route("/profile", methods=['GET'])
@login_required
def client_profile():
    email = current_user.email;
    client_info = get_client_info(current_user.id)
    previous_rides = get_all_previous_rides(current_user.id)
    if current_user.role == 'client':
        return render_template('profile.html', email = email, client_info = client_info,previous_rides=previous_rides)

@client_bp.route("/profile/update", methods=['POST'])
@login_required
def update_client_profile():
    start_time = time.time()
    name = request.form.get('name')
    email = request.form.get('email')
    address = request.form.get('address')
    sql_id = current_user.id
    if email != current_user.email:
        add_client_email(sql_id, email)
    if name != '':
        add_client_name(sql_id,name)
    if address != '':
        add_client_address(sql_id, address)
    end_time = time.time()
    elapsed_time = end_time-start_time
    time_logger.info(f"Route: /profile/update - Time taken: {elapsed_time:.6f} seconds")
    return redirect(url_for('client.client_profile'))

