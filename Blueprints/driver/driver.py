from flask import Blueprint, render_template, request, redirect, url_for,session,jsonify
from flask_login import login_required, current_user
from Database.MongoDB.driver import add_driver_details, is_verified,form_filled,get_driver_details, add_driver_fname, add_driver_lname,add_driver_email
from Database.MongoDB.rides import assign_driver,get_ride_details,get_otp,update_status,get_ride_status,get_all_previous_rides
from Helpers.OTP.otp import verify_otp
from Database.SQL.client import add_user
from Class.authentication.classes import RegistrationForm
from flask_bcrypt import Bcrypt
import time
from logger.log import time_logger

driver_bp = Blueprint("driver", __name__, template_folder="templates")
bcrypt = Bcrypt()

@driver_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print('this is a get in driver')
    if form.validate_on_submit():
        print('registering')
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        role = 'driver'
        print(role,'registering the driver ')
        add_user(email, hashed_password, role)
            
    return render_template('driverregister.html', form=form)

@driver_bp.route("/", methods=['GET'])
@login_required
def driver():
    if current_user.role == 'driver':
        if form_filled(current_user.id):
            return redirect(url_for('driver.driver_space'))
        return render_template('driver.html')

@driver_bp.route("/workspace", methods=['GET'])
@login_required
def driver_space():
    if current_user.role == 'driver':
        if is_verified(current_user.id):
            return render_template('workspace.html')
        return render_template('driverView.html')

@driver_bp.route("/information", methods=['POST'])
@login_required
def driver_information():
# do it later
    if current_user.role == 'driver':
        id = current_user.id
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email=current_user.email
        driveCity = request.form.get('city')
        vehicleType = request.form.get('vehicleType')
        identity_file = request.files.get('identity')
        driver_photo = request.files.get('photo')
        kbis_file = request.files.get('Kbis')
        license = request.files.get('license')
        vehicle_photo = request.files.get('vehicle')
        birthCertificate = request.files.get('dob')
            
        # print(id, email, driveCity, vehicleType, identity_file, driver_photo,kbis_file, license, vehicle_photo,birthCertificate)
        add_driver_details(id, firstname, lastname,email, driveCity, vehicleType, identity_file, driver_photo,kbis_file, license, vehicle_photo,birthCertificate)
        return redirect(url_for('driver.driver_space'))

# display a notification in driver space if any request has been made and if any driver has accepted it
@driver_bp.route("/accept_ride/<ride_id>", methods=['POST'])
@login_required
def accept_ride(ride_id):
# do it later
    # the ride has been accepted
    start_time = time.time()
    if current_user.role == 'driver':
        assign_driver(ride_id, current_user.id)
        end_time = time.time()
        elapsed_time = end_time-start_time
        time_logger.info(f"Route: / - Time taken: {elapsed_time:.6f} seconds")
        return 'Accepted'
    

# if the driver has accepted the ride
@driver_bp.route("/ride/<ride_id>", methods=['GET'])
@login_required
def riding(ride_id):
    # we need the ride pickup and dropoff location
    # also the otp verification
    # make sure only the driver related to the ride  can access this
    start_time = time.time()
    ride_data = get_ride_details(ride_id)
    session['driver_satus'] = 'busy'
    session['ride_id'] = ride_id
    ride_status = get_ride_status(ride_id)
    if current_user.role == 'driver':
        end_time = time.time()
        elapsed_time = end_time-start_time
        # put route name  /ride/<ride_id> as well in the logger
        time_logger.info(f"Route: /ride/{ride_id} - Time taken: {elapsed_time:.6f} seconds")
        return render_template('driverRide.html',ride_data = ride_data, status = ride_status)
    
@driver_bp.route("/ride/<ride_id>/<otp>", methods=['POST'])
@login_required
def verify_otp_db(ride_id,otp):
    start_time = time.time()
    og_otp = get_otp(ride_id)
    response = verify_otp(otp, og_otp)
    # ride has started
    update_status('Started',ride_id)
    print(response)
    if response:
        end_time = time.time()
        elapsed_time = end_time-start_time
        time_logger.info(f"Route: /ride/{ride_id}/{otp} - Time taken: {elapsed_time:.6f} seconds")
        return jsonify({'success': True, 'message': 'OTP verification successful'})
    else:
        end_time = time.time()
        elapsed_time = end_time-start_time
        time_logger.info(f"Route: /ride/{ride_id}/{otp} - Time taken: {elapsed_time:.6f} seconds")
        return jsonify({'success': False, 'message': 'OTP verification failed'})
    
@driver_bp.route("/profile", methods=['GET'])
@login_required
def driver_profile():
    driver_info = get_driver_details(current_user.id)
    previous_rides = get_all_previous_rides(current_user.id)
    return render_template('driverProfile.html', driver_info = driver_info, previous_rides = previous_rides )
    
@driver_bp.route("/profile/update", methods=['POST'])
@login_required
def update_driver_profile():
    start_time = time.time()
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    print(fname,lname,email)
    sql_id = current_user.id
    if email != current_user.email:
    
        add_driver_email(sql_id, email)
    if fname != '':
       
        add_driver_fname(sql_id,fname)
    if lname != '':
        add_driver_lname(sql_id,lname)

    end_time = time.time()
    elapsed_time = end_time-start_time
    time_logger.info(f"Route: /profile/update - Time taken: {elapsed_time:.6f} seconds")
    return redirect(url_for('driver.driver_profile'))


    
