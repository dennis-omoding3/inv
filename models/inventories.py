from app import db


class InventoryModel(db.Model):
    # create a table name
    __tablename__ = 'inventories'
    # creating the columns of your table and passing the type; string has the max length
    id = db.Column(db.Integer, primary_key=True)
    inv_name = db.Column(db.String(50), nullable=False)
    inv_type = db.Column(db.String, nullable=False)
    bp = db.Column(db.Float, nullable=False)
    sp = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    rp = db.Column(db.Integer, nullable=False)
    sales = db.relationship('SalesModel', backref='Inventory', lazy=True)  # creates the foreign key

    @classmethod
    def update_stock(cls, id, sl_qt):
        record = InventoryModel.query.filter_by(id=id).first()
        if record:
            if sl_qt > record.stock:
                return False
            else:
                record.stock = record.stock - sl_qt
            db.session.commit()
            return True
        else:

            return False

        # edit record

    @classmethod
    def edit_record(cls,id, inv_name, inv_type, bp, sp, stock, rp):
        record = cls.query.filter_by(id=id).first()
        if record:
            record.inv_name = inv_name
            record.inv_type = inv_type
            record.bp = bp
            record.sp = sp
            record.stock = stock
            record.rp = rp

            db.session.commit()
            return True
        else:
            return False
    @classmethod
    def getTypeCount(cls,name):
        record = cls.query.filter_by(inv_type=name).count()
        return record
# connect the application to the
#     @classmethod
#     def delete_entry(cls):
#         entry=cls.query.filter_by(id=id).first()
#         if entry:
#             db.session.delete(entry)
#             db.session.commit()
#             return True
