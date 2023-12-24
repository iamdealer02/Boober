from flask import Blueprint, render_template, request, redirect, url_for,session,jsonify
from flask_login import login_required, current_user
from Database.MongoDB.driver import add_driver_details, is_verified,form_filled,get_driver_details, add_driver_fname, add_driver_lname,add_driver_email
from Database.MongoDB.rides import assign_driver,get_ride_details,get_otp,update_status,get_ride_status,get_all_previous_rides
from Helpers.OTP.otp import verify_otp, generate_hotp, generate_random_secret_key
from Database.SQL.client import add_user
from Class.authentication.classes import RegistrationForm
from flask_bcrypt import Bcrypt
from flask_mail import Message
from SMTP.mail_init import mail
import os
driver_bp = Blueprint("driver", __name__, template_folder="templates")
bcrypt = Bcrypt()


@driver_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method=='POST' and form.validate_on_submit():
        print('registering')
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        role = 'driver'
        otp = generate_hotp(generate_random_secret_key())
        session['otp'] = otp
        message_send= False
        # confirmation mail about the posting of recipe
        if message_send == False:
            msg = Message('YOUT OTP', sender='no_reply@app.com', recipients=[email])
            msg.body = f'THANKYOU FOR REGISTERING TO OUR SERVICE. PLEASE CONFIRM YOUR EMAIL BY ENTERING THE OTP! YOUR OTP IS {otp}'
            mail.send(msg)
            message_send = True
        print('redirecting')
        return redirect(url_for('driver.verify', email=email, hashed_password=hashed_password, role=role))
        
    return render_template('driverregister.html', form=form)

@driver_bp.route("/register/verify/<email>/<hashed_password>/<role>", methods=['GET', 'POST'])
def verify(email, hashed_password,role):
    if request.method == 'POST':
        print('verifying')
        digit1 = request.form.get('digit1')
        digit2 = request.form.get('digit2')
        digit3 = request.form.get('digit3')
        digit4 = request.form.get('digit4')
        digit5 = request.form.get('digit5')
        digit6 = request.form.get('digit6')
        otp = digit1 + digit2 + digit3 + digit4 + digit5 + digit6
        otp = int(otp)
        print(otp)
        print(session['otp'])
        if int(session['otp']) ==  otp:
            add_user(email, hashed_password, role)
            return redirect(url_for('authentication.login'))
        else:
            print('OTP not verified')
            return render_template('verify.html')
    return render_template('verify.html')


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
    if current_user.role == 'driver':
        assign_driver(ride_id, current_user.id)
        return 'Accepted'
    

# if the driver has accepted the ride
@driver_bp.route("/ride/<ride_id>", methods=['GET'])
@login_required
def riding(ride_id):
    MAP_API_KEY = os.getenv("MAP_API_KEY")
    # we need the ride pickup and dropoff location
    # also the otp verification
    # make sure only the driver related to the ride  can access this
    ride_data = get_ride_details(ride_id)
    session['driver_satus'] = 'busy'
    session['ride_id'] = ride_id
    ride_status = get_ride_status(ride_id)
    if current_user.role == 'driver':
        return render_template('driverRide.html',ride_data = ride_data, status = ride_status, MAP_API_KEY=MAP_API_KEY)
    
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
    
@driver_bp.route("/profile", methods=['GET'])
@login_required
def driver_profile():
    driver_info = get_driver_details(current_user.id)
    previous_rides = get_all_previous_rides(current_user.id)
    return render_template('driverProfile.html', driver_info = driver_info, previous_rides = previous_rides )
    
@driver_bp.route("/profile/update", methods=['POST'])
@login_required
def update_driver_profile():
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

   
    return redirect(url_for('driver.driver_profile'))

@driver_bp.route("/ride/finish/<ride_id>", methods=['GET'])
@login_required
# update status to completed and send invoice mail to the client
def finish_ride(ride_id):
    update_status('Completed',ride_id)
    # send invoice mail to the client 
    ride_data = get_ride_details(ride_id)   
    return redirect(url_for('driver.invoice', ride_data = ride_data))  


@driver_bp.route("/invoice/<ride_id>", methods=['GET'])
@login_required
def invoice(ride_id):
    MAP_API_KEY = os.getenv("MAP_API_KEY")
    ride_data = get_ride_details(ride_id)
    return render_template('invoice.html', ride_data = ride_data, MAP_API_KEY=MAP_API_KEY)
    