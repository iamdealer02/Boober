from flask import Blueprint, render_template, request, redirect, url_for,session,jsonify
from flask_login import login_required, current_user
from Database.MongoDB.driver import add_driver_details, is_verified,form_filled
from Database.MongoDB.rides import assign_driver,get_ride_details,get_otp,update_status,get_ride_status
from Helpers.OTP.otp import verify_otp
from Database.SQL.client import add_user
from Class.authentication.classes import RegistrationForm
from flask_bcrypt import Bcrypt
# from flask_socketio import SocketIO

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
        add_driver_details(id, email, driveCity, vehicleType, identity_file, driver_photo,kbis_file, license, vehicle_photo,birthCertificate)
        return redirect(url_for('driver.driver_space'))

# display a notification in driver space if any request has been made and if any driver has accepted it
@driver_bp.route("/accept_ride/<ride_id>", methods=['POST'])
@login_required
def accept_ride(ride_id):
# do it later
    # the ride has been accepted
    if current_user.role == 'driver':
        assign_driver(ride_id, current_user.id)
        return 'Accepted'
    

# if the driver has accepted the ride
@driver_bp.route("/ride/<ride_id>", methods=['GET'])
@login_required
def riding(ride_id):
    # we need the ride pickup and dropoff location
    # also the otp verification
    # make sure only the driver related to the ride  can access this
    ride_data = get_ride_details(ride_id)
    session['driver_satus'] = 'busy'
    session['ride_id'] = ride_id
    ride_status = get_ride_status(ride_id)
    if current_user.role == 'driver':
        return render_template('driverRide.html',ride_data = ride_data, status = ride_status)
    
@driver_bp.route("/ride/<ride_id>/<otp>", methods=['POST'])
@login_required
def verify_otp_db(ride_id,otp):
    og_otp = get_otp(ride_id)
    response = verify_otp(otp, og_otp)
    # ride has started
    update_status('Started',ride_id)
    print(response)
    if response:
            return jsonify({'success': True, 'message': 'OTP verification successful'})
    else:
        return jsonify({'success': False, 'message': 'OTP verification failed'})
    

    
