import bcrypt
from flask import Flask 
import os
from flask_wtf import form
from flaskwebgui import FlaskUI
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os
from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mailman import Mail

app = Flask(__name__)
csrf=CSRFProtect()
csrf.init_app(app)
this_file_path = os.path.abspath(os.path.dirname(__file__))
base_dir = os.path.abspath(os.path.dirname(this_file_path))
chromium_path = f"{base_dir}/bin/chrome.exe"
# chromium_path = f"{this_file_path}/bin/chrome.exe"
# ui = FlaskUI(app,browser_path = chromium_path) # add app and parameters
# ui = FlaskUI(app) # add app and parameters
ui = FlaskUI(app, width=500, height=500,browser_path = chromium_path) # add app and parameters

app.config['SECRET_KEY'] = 'ec5a692b16718cb07a72537a685c0689'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site1.db' # site1.db create on directory where the __init__ file placed
app.permanent_session_lifetime = timedelta(seconds=5)
app.config['WTF_CSRF_ENABLED'] = False
app.config['WTF_CSRF_SECRET_KEY'] = '$2b$12$EOH89ayJXH6eBj9I7JSnvOU.Lp5LDWCtZx6sl2133YI05lkmd42JKb8d.'
app.config['PERMANENT_SESSION_LIFE_TIME'] = timedelta(days=5) # make session.permanent = True in a route fn
# app.config['SQLALCHEMY_DATABASE_URI'] = create_engine('sqllite:///site.db')
app.config['MAIL_SERVER'] = 'smtp.google.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "schnellsystem123@gmail.com"
app.config['MAIL_PASSWORD'] = "schnellsystem321"
mail = Mail(app)


db = SQLAlchemy(app)
    # Need to initalize the routes contain path to all the html pages
bcrypt_app = Bcrypt(app)
# app.secret_key = 'jdsjfakgkjgaj'
login_manager = LoginManager(app)
login_manager.init_app(app)

login_manager.login_message_category = 'info'
login_manager.login_view = 'login'
login_manager.session_protection = 'strong'
