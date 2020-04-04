from database import db

db.Model.metadata.reflect(db.engine)


class Artists(db.Model):
    __table__ = db.Model.metadata.tables['artists']


class Records(db.Model):
    __table__ = db.Model.metadata.tables['records']


class Songs(db.Model):
    __table__ = db.Model.metadata.tables['songs']


class Users(db.Model):
    __table__ = db.Model.metadata.tables['users']


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