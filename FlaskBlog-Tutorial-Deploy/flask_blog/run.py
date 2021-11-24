
from sqlalchemy.sql.sqltypes import Time
from flaskblog_package import app, ui
# from flaskblog_package.models import init_db  
# can import routes in init or run.py 
from flaskblog_package import routes

from flask import Flask
from flaskwebgui import FlaskUI
from threading import Thread, Timer
import time


if __name__ == '__main__':
        # while User table does not found call init_db()
    # init_db()  
    # installing waitress for retain app window
    # Timer(1, ui.keep_server_running).start()
    # ui.run()
    # while True:
    #     ui.keep_server_running()
    #     time.sleep(2)
    # ui.keep_server_running()
    app.run(debug= True)
