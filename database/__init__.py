from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'O38mjKm7q-b9Sz_8D6oYBA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///record_store.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dklintworth:8%c@@JP$%N33@localhost/record_store'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from database.models import *

rec = []

db.create_all()


from database.routes import *
