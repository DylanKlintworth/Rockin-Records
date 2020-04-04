from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'O38mjKm7q-b9Sz_8D6oYBA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dklintworth:8%c@@JP$%N33@localhost/record_store'
db = SQLAlchemy(app)

from database import models
from database import routes

models.db.create_all()

