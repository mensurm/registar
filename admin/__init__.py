# -*- coding: utf-8 -*-
__author__ = 'mensur'

from flask import Flask
from models import db, User, Role
from flask.ext.security import Security, SQLAlchemyUserDatastore
from config import SECRET_KEY


from flask_sqlalchemy import SQLAlchemy

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config.from_object('config')

db.init_app(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

#user_datastore.create_user(email='dzukaman@hotmail.com', password='password', firstname='Mujo', lastname='Mujic', real_email='mensur.mandzuka@gmail.com')
#db.session.commit()
import routes

