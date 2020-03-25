from db import db, ma

class StoreModel(db.Model):
    __tablename__ = 'stores'

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    items = db.relationship('ItemModel', backref='stores', lazy=True)

    def __repr__(self):
        return f'<Store {self.name}>'



class StoreSchema(ma.Schema):
    class Meta:
        fields = ('_id', 'name', 'items')

    items = ma.List(ma.Nested("ItemSchema", only=("_id", "name", "price")))