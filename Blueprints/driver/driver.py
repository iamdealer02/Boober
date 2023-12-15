from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from Database.MongoDB.driver import add_driver_details, is_verified,form_filled
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
    print(form_filled(current_user.id))
    if form_filled(current_user.id):
        return redirect(url_for('driver.driver_space'))
    return render_template('driver.html')

@driver_bp.route("/workspace", methods=['GET'])
@login_required
def driver_space():
    print(is_verified(current_user.id))
    if is_verified(current_user.id):
        print('has filled the form and is verified')
        return render_template('workspace.html')
    return render_template('driverView.html')

@driver_bp.route("/information", methods=['POST'])
@login_required
def driver_information():
# do it later
    id = 1
    email='kjhfjs'
    driveCity = request.form.get('city')
    print(driveCity)
    vehicleType = request.form.get('vehicleType')
    print(vehicleType)
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