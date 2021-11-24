from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms.form import Form
from wtforms.validators import ValidationError
from wtforms import validators
from wtforms.fields.simple import PasswordField, StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flaskblog_package.models import User
from flask_login import current_user

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


            