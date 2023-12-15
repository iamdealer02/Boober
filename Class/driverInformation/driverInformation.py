
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, HiddenField
from wtforms.validators import InputRequired

class MultiStepForm(FlaskForm):
    city = StringField('Where would you like to earn?', validators=[InputRequired()])
    ReferralCode = StringField('Referral Code (optional)')
    vehicleType = HiddenField('Vehicle Type')

    identity = FileField('Piece of valid Identity', validators=[InputRequired()])
    photo = FileField('Your Photo of face in center with good lighting', validators=[InputRequired()])
    Kbis = FileField('Extrait KBIS', validators=[InputRequired()])
    license = FileField('License', validators=[InputRequired()])
    vehicle = FileField('Photo of Vehicle', validators=[InputRequired()])
    dob = FileField('Birth-Certificate', validators=[InputRequired()])