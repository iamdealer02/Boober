from flask import *
from flask_caching import Cache
from flask_mail import *
from flask_babel import *
from Database.SQL.client import get_user_by_id
from Class.authentication.classes import User
from flask_login import LoginManager, current_user
from SMTP.mail_init import init_mail
import time
from logger.log import time_logger, auth_logger
from dotenv import load_dotenv
import os

# getting the blueprints
from Blueprints.home.home import home_bp
from Blueprints.authentication.authentication import authentication_bp
from Blueprints.client.client import client_bp
from Blueprints.driver.driver import driver_bp
from Blueprints.map.map import map_bp
from Blueprints.sockets.sockets import sockets_bp, socketio
from Blueprints.admin.admin import admin_bp

app = Flask(__name__)
load_dotenv()


app.secret_key = os.getenv("SECRET_KEY")
app.debug = True

# configuring the cache
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

babel = Babel(app)
init_mail(app)

login_manager = LoginManager()
login_manager.login_view = 'authentication.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    data = None
    data = get_user_by_id(user_id)

    if data and len(data) >= 3:


        return User(data[0],data[1],data[3])
    else:

        return None
    

# registering all the Blueprints
app.register_blueprint(authentication_bp)
app.register_blueprint(home_bp)
app.register_blueprint(client_bp,url_prefix="/client")
app.register_blueprint(driver_bp,url_prefix="/driver")
app.register_blueprint(map_bp)
app.register_blueprint(sockets_bp)
app.register_blueprint(admin_bp, url_prefix = "/admin")



# INTEGRATING MIDDLEWARES FOR LOGGING AND PERFORMANCE TRACKING OF THE APPLICATION 
# before and after request for performance tracking of every route
@app.before_request
def before_request():
    g.start = time.time()
    
@app.after_request
def after_request(response):
    elapsed_time = time.time() - g.start
    # put this in time_logger file
    time_logger.info(f"Route: {request.endpoint}, "
        f"Method: {request.method}, "
        f"Status: {response.status_code}, "
        f"Time: {elapsed_time:.6f} seconds")
    # if the route is login or logout then log it in the authentication.log file
    # with the user email logged in or logged out
    # Check if the route is related to authentication

    if request.endpoint in ['authentication.login', 'authentication.logout']:
        user_email = g.get('user_email', 'Unknown')

        auth_logger.info(
            f"Route: {request.endpoint}, "
            f"Method: {request.method}, "
            f"Status: {response.status_code}, "
            f"User: {user_email}, "
            f"Time: {elapsed_time:.6f} seconds"
        )

    return response

@app.teardown_appcontext
def close_connection(exception): 
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()




if __name__ == '__main__':
    socketio.init_app(app)
    socketio.run(app, debug=True)
    
