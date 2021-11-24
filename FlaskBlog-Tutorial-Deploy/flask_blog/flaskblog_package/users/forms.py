from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms.form import Form
from wtforms.validators import ValidationError
from wtforms import validators
from wtforms.fields.simple import PasswordField, StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flaskblog_package.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired(), Length(min=2, max= 20)])
    email  = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):        
        user = User.query.filter_by(username= username.data).first()
        if user:
            raise ValidationError('That username is already taken please choose another')
    def validate_email(self,email):
        user = User.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError('Email address is alredy taken , Please choose another')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('password',validators=[ DataRequired()])
    remember = BooleanField('Remeber Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired(), Length(min=2, max= 20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    email  = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

    def validate_username(self, username):  
        if username.data != current_user.username:
            user = User.query.filter_by(username= username.data).first()
            if user:
                raise ValidationError('That username is already taken please choose another')
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email= email.data).first()
            if user:
                raise ValidationError('Email address is alredy taken , Please choose another')


class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Request submit')

    def validate_email(self,email):
        user = User.query.filter_by(email= email.data).first()
        if user is None:
            raise ValidationError('There is no Account with that email address. You must register')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('password reset ')
