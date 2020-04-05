from database import db, login_manager
from flask_login import UserMixin

db.Model.metadata.reflect(db.engine)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Artists(db.Model):
    __table__ = db.Model.metadata.tables['artists']


class Records(db.Model):
    __table__ = db.Model.metadata.tables['records']


class Songs(db.Model):
    __table__ = db.Model.metadata.tables['songs']


class Users(db.Model, UserMixin):
    __table__ = db.Model.metadata.tables['users']

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"Email: {self.email}"


class Employees(db.Model):
    __table__ = db.Model.metadata.tables['employees']


class Stores(db.Model):
    __table__ = db.Model.metadata.tables['stores']


class Orders(db.Model):
    __table__ = db.Model.metadata.tables['orders']


class Record_Sales(db.Model):
    __table__ = db.Model.metadata.tables['record_sales']


class Inventory(db.Model):
    __table__ = db.Model.metadata.tables['inventory']
