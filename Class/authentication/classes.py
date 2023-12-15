from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from Database.SQL.client import is_email_taken
from flask_login import  UserMixin


class User(UserMixin):
    def __init__(self,id,email,role):
         self.id = id
         self.email = email
         self.role = role  
         self.authenticated = False
    def is_active(self):
         return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.id   




class RegistrationForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                     EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_email(form, field):
        if is_email_taken(field.data):
            print("error")
            raise ValidationError('Email already taken')
        
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

