from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sebastian:pass123@localhost/flask_restful_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

api = Api(app)

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

items_schema = ItemSchema(many=True)
item_schema = ItemSchema()

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('price', type=float, required=True)


class Items(Resource):
    def get(self):
        items = ItemModel.query.all()

        return {'items': items_schema.dump(items)}, 200

    def post(self):
        data = parser.parse_args()
        item = ItemModel(**data)

        db.session.add(item)
        db.session.commit()

        return {'item': item_schema.dump(item)}, 201

class Item(Resource):
    def get(self, id):
        item = ItemModel.query.filter_by(id = id).first_or_404(f'No item with id: {id}')

        return {'item': item_schema.dump(item)}, 200

    def put(self, id):
        item = ItemModel.query.filter_by(id = id).first_or_404(f'No item with id: {id}')

        data = parser.parse_args()
        for key, val in data.items():
            setattr(item, key, val)

        db.session.commit()
        
        return {'item': item_schema.dump(item)}, 201

    def delete(self, id):
        item = ItemModel.query.filter_by(id = id).first()

        db.session.delete(item)
        db.session.commit()

        return {'message': 'item deleted'}, 200
        

api.add_resource(Items, '/items', endpoint='items')
api.add_resource(Item, '/items/<id>', endpoint='item')

