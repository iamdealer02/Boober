from flask import Flask, render_template, redirect, url_for, Blueprint,send_file, current_app
from flask_login import login_user, current_user, login_required
from flask_bcrypt import Bcrypt
from Class.authentication.classes import LoginForm, User
from Database.SQL.client import check_user
from Database.MongoDB.driver import get_non_verified_drivers,get_driver_details,get_media,verify_driver
from werkzeug.utils import secure_filename



bcrypt = Bcrypt()

admin_bp = Blueprint("admin", __name__, template_folder="templates")



@admin_bp.route("/login", methods=['GET', 'POST'])
def adminLogin():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        admin = check_user(email)
        if admin and (admin[2] == password):
            login_user(User(admin[0], admin[1], admin[3]))
            return redirect(url_for('admin.adminPage'))

    return render_template('adminLogin.html', form=form)

@admin_bp.route("/")
@login_required
def adminPage():
    if current_user.role == 'admin':
        drivers = get_non_verified_drivers()
        return render_template('adminWorkspace.html', drivers = drivers)
    else:
        return redirect(url_for('admin.adminLogin'))


@admin_bp.route("/driverFile/<driver_id>")
@login_required
def driverFile(driver_id):
    driver = get_driver_details(driver_id)
    return render_template('driverFile.html', driver=driver)

@admin_bp.route('/get_media/<media_id>')
@login_required
def get_media_flask(media_id):
    media_data, media_mime, filename = get_media(media_id)
    return send_file(
        media_data,
        mimetype=media_mime,
        as_attachment=True,
        download_name=secure_filename(filename)
    )

@admin_bp.route('/routes')
@login_required
def detail_routes():
    if current_user.role == 'admin':
        with current_app.test_request_context():
            routes = []
            for rule in current_app.url_map.iter_rules():
                route = {
                    'endpoint': rule.endpoint,
                    'methods': sorted(rule.methods),
                    'path': str(rule)
                }
                routes.append(route)
        return render_template('routes.html', routes=routes)

@admin_bp.route('/verify/<driver_id>', methods=['POST'])
@login_required
def verify(driver_id):
    if current_user.role == 'admin':
        verify_driver(driver_id)
        return redirect(url_for('admin.adminPage'))
    
@admin_bp.route('/performance')
@login_required
def performance():
    if current_user.role == 'admin':
        #read elapsed time from log file
        #read log file
        #parse the log file
        #get the elapsed time
        #return the elapsed time
        open_file = open('elapsed_time.log', 'r')
        lines = open_file.readlines()
        open_file.close()
        return render_template('performance.html', lines=lines)
