from flask import *
from flask_caching import Cache
from flask_mail import *
from flask_babel import *
from Database.SQL.client import get_user_by_id
from Class.authentication.classes import User
from flask_login import LoginManager

# getting the blueprints
from Blueprints.home.home import home_bp
from Blueprints.authentication.authentication import authentication_bp
from Blueprints.client.client import client_bp
from Blueprints.driver.driver import driver_bp
from Blueprints.map.map import map_bp
from Blueprints.sockets.sockets import sockets_bp, socketio
from Blueprints.admin.admin import admin_bp

app = Flask(__name__)



app.secret_key = 'upasana12345'
app.debug = True



babel = Babel(app)

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




@app.teardown_appcontext
def close_connection(exception): 
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    socketio.init_app(app)
    socketio.run(app, debug=True)
    
