from database import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
#db.Model.metadata.reflect(db.engine)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

Record_Sales_Table = db.Table('record_sales', db.Model.metadata,
		db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
		db.Column('record_id', db.Integer, db.ForeignKey('records.id'))
	)

class Artists(db.Model):
    # __table__ = db.Model.metadata.tables['artists']
	id = db.Column(db.Integer, primary_key=True)
	artist_name = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return f"Artist: '{self.artist_name}'"

class Records(db.Model):
    # __table__ = db.Model.metadata.tables['records']
	id = db.Column(db.Integer, primary_key=True)
	record_name = db.Column(db.String(120), nullable=False)
	record_genre = db.Column(db.String(120), nullable=False)
	record_genre = db.Column(db.String(120), nullable=False)
	record_price = db.Column(db.Float, nullable=False)
	artist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	orders = relationship("Orders", secondary=Record_Sales_Table, back_populates="records")
	
	def __repr__(self):
		return f"Record: '{self.record_name}, Genre: '{self.record_genre}'" 

class Songs(db.Model):
    # __table__ = db.Model.metadata.tables['songs']
	id = db.Column(db.Integer, primary_key=True)
	song_name = db.Column(db.String(120), nullable=False)
	record_id = db.Column(db.Integer, db.ForeignKey('record.id'), nullable=False)
	song_length = db.Column(db.String(10))
	
	def __repr__(self):
		return f"Song: '{self.song_name}'"
	
class Users(db.Model):
    # __table__ = db.Model.metadata.tables['users']
	id = db.Column(db.Integer, primary_key=True)
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
	id = db.Column(db.Integer, primary_key=True)
	street_address = db.Column(db.String(120))
	city_address = db.Column(db.String(120))
	state_address = db.Column(db.String(120))
	zip_address = db.Column(db.String(120))

class Employees(db.Model):
    # __table__ = db.Model.metadata.tables['employees']
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(120), nullable=False)
	last_name = db.Column(db.String(120), nullable=False)
	birth_date = db.Column(db.String(10))
	street_address = db.Column(db.String(120))
	city_address = db.Column(db.String(120))
	state_address = db.Column(db.String(120))
	zip_address = db.Column(db.String(120))
	phone_number = db.Column(db.String(15))
	job_title = db.Column(db.String(120), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)

class Orders(db.Model):
    # __table__ = db.Model.metadata.tables['orders']
	id = db.Column(db.Integer, primary_key=True)
	order_date = db.Column(db.String())
	employee_id = store_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	
	records = relationship("Records", secondary=Record_Sales_Table, back_populates="orders")
	
# class Record_Sales(db.Model):
#    # __table__ = db.Model.metadata.tables['record_sales']
#	id = db.Column(db.Integer, primary_key=True)
	

class Inventory(db.Model):
    # __table__ = db.Model.metadata.tables['inventory']
	id = db.Column(db.Integer, primary_key=True)
	record_id = db.Column(db.Integer, db.ForeignKey('records.id'), nullable=False)
	store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
	
	