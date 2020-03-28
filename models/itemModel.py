from db import db, ma

class ItemModel(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'),
        nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'

class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price', 'store_id')

    # _links = ma.Hyperlinks(
    #     {"self": ma.URLFor('item', _id="<_id>"), "collection": ma.URLFor('items')}
    # )