
from datetime import datetime
from app import db


class SalesModel(db.Model):
    # create a table name
    __tablename__ = 'sales'
    # creating the columns of your table and passing the type; string has the max length
    id = db.Column(db.Integer, primary_key=True)
    sl_qt = db.Column(db.Integer, nullable=False)
    inv_id = db.Column(db.Integer, db.ForeignKey('inventories.id'))
    time_created = db.Column(db.DateTime,default=datetime.utcnow())
