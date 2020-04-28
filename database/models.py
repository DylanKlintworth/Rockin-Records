from database import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


# db.Model.metadata.reflect(db.engine)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class RecordSales(db.Model):
    record_id = db.Column(db.Integer, db.ForeignKey('records.record_id'), primary_key=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), primary_key=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class Artists(db.Model):
    # __table__ = db.Model.metadata.tables['artists']
    artist_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement="auto")
    artist_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Artist: '{self.artist_name}'"


class Records(db.Model):
    # __table__ = db.Model.metadata.tables['records']
    record_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement="auto")
    record_name = db.Column(db.String(120), nullable=False)
    record_genre = db.Column(db.String(120), nullable=False)
    record_price = db.Column(db.Float, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'), nullable=False)

    def __repr__(self):
        return f"Record: '{self.record_name}', Genre: '{self.record_genre}'"


class Songs(db.Model):
    # __table__ = db.Model.metadata.tables['songs']
    song_id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    song_name = db.Column(db.String(120), nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('records.record_id'), nullable=False)
    song_length = db.Column(db.String(10))

    def __repr__(self):
        return f"Song: '{self.song_name}'"


class Users(db.Model, UserMixin):
    # __table__ = db.Model.metadata.tables['users']
    user_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement="auto")
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    street_address = db.Column(db.String(120))
    city_address = db.Column(db.String(120))
    state_address = db.Column(db.String(120))
    zip_address = db.Column(db.String(120))
    phone_number = db.Column(db.String(15))

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"Email: {self.email}"


class Stores(db.Model):
    # __table__ = db.Model.metadata.tables['stores']
    store_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement="auto")
    store_name = db.Column(db.String(120), nullable=False)
    street_address = db.Column(db.String(120), nullable=False)
    city_address = db.Column(db.String(120), nullable=False)
    state_address = db.Column(db.String(120), nullable=False)
    zip_address = db.Column(db.String(120), nullable=False)


class Employees(db.Model):
    # __table__ = db.Model.metadata.tables['employees']
    employee_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement="auto")
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.Date)
    street_address = db.Column(db.String(120))
    city_address = db.Column(db.String(120))
    state_address = db.Column(db.String(120))
    zip_address = db.Column(db.String(120))
    phone_number = db.Column(db.String(15))
    job_title = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'), nullable=False)
    salary = db.Column(db.Float)
    hourly_rate = db.Column(db.Float)


class Orders(db.Model):
    # __table__ = db.Model.metadata.tables['orders']
    order_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement="auto")
    order_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'), nullable=False)


class Inventory(db.Model):
    record_id = db.Column(db.Integer, db.ForeignKey('records.record_id'), primary_key=True, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'), primary_key=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class UserCart:

    def __init__(self):
        self.cart = []

    def get_cart(self):
        return self.cart

    def add_record(self, record):
        self.cart.append(record)
