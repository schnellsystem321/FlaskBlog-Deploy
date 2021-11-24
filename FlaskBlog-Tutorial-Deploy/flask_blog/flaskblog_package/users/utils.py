
import secrets,os
from flaskblog_package.models import User, Post  # after initializing the main(__name__) and db import from models
from flaskblog_package import app
from PIL import Image
from flask import url_for
from flask_mailman import EmailMessage



def save_picture(form_picture):
    random = secrets.token_hex(8)
    _, f_ext =  os.path.splitext(form_picture.filename)
    picture_fn = random + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn



def send_reset_email(user):
    token = user.get_reset_token()
    print(token,user.email,'rrrrrrrrrrrrrrrrr')
    message = EmailMessage('Password reset request','schnellsystem123@gmail.com','schnellsystem123@gmail.com')
    message.body = f'''to reset your password  visit the following link :
                    { url_for('reset_token',token=token, _external= True)}
                    If you did not make this request then no change occurs
                    '''
    mail_send = message.send(message)
    print(mail_send,'{{{{{{{{')