from flask import Blueprint, render_template, redirect,request
from flask_login import login_required, current_user
from Class.authentication.classes import RegistrationForm
from flask_bcrypt import Bcrypt
from Database.SQL.client import add_user

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
    return render_template('client.html')

@client_bp.route("/ride", methods=['POST'])
@login_required
def handle_ride_data():
    data = request.form
    # Process the data as needed
    print('Received data:', data)
    return 'Data received successfully'

# @socketio.on('ride_request')
# def handle_ride_request(data):
#     # Broadcast the ride request to all connected drivers
#     socketio.emit('new_ride_request', data, namespace='/drivers')
