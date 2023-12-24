from flask_mail import Mail

mail = Mail()

def init_mail(app):
    app.config['MAIL_SERVER']='smtp.gmail.com'  
    app.config['MAIL_PORT']=465  
    app.config['MAIL_USERNAME'] = 'sharmaupasana823@gmail.com'  
    app.config['MAIL_PASSWORD'] = 'xkkzgbuvozqhrhmf'  
    app.config['MAIL_USE_TLS'] = False  
    app.config['MAIL_USE_SSL'] = True  
    
    mail.init_app(app)
