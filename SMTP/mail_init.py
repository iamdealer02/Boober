from flask_mail import Mail
import os
mail = Mail()

def init_mail(app):
    app.config['MAIL_SERVER']=os.getenv("MAIL_SERVER") 
    app.config['MAIL_PORT']=  os.getenv("MAIL_PORT")
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_USE_TLS'] = False  
    app.config['MAIL_USE_SSL'] = True  
    
    mail.init_app(app)
