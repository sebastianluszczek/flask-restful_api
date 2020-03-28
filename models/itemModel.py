from db import db, ma

class ItemModel(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'

class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price', '_links')

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {"self": ma.URLFor('item', id="<id>"), "collection": ma.URLFor('items')}
    )