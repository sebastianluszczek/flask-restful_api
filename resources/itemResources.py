from flask_restful import Resource, reqparse

from db import db

from models.itemModel import ItemModel, ItemSchema

from flask_jwt import jwt_required

items_schema = ItemSchema(many=True)
item_schema = ItemSchema()

item_parser = reqparse.RequestParser()
item_parser.add_argument('name', type=str, required=True)
item_parser.add_argument('price', type=float, required=True)
item_parser.add_argument('store_id', type=int, required=True)

class Items(Resource):
    def get(self):
        items = ItemModel.query.all()

        return {'items': items_schema.dump(items)}, 200

    @jwt_required()
    def post(self):
        data = item_parser.parse_args()
        item = ItemModel(**data)

        db.session.add(item)
        db.session.commit()

        return {'item': item_schema.dump(item)}, 201

class Item(Resource):
    def get(self, id):
        item = ItemModel.query.filter_by(id = id).first_or_404(f'No item with id: {id}')

        return {'item': item_schema.dump(item)}, 200

    @jwt_required()
    def put(self, id):
        item = ItemModel.query.filter_by(id = id).first_or_404(f'No item with id: {id}')

        data = item_parser.parse_args()
        for key, val in data.items():
            setattr(item, key, val)

        db.session.commit()
        
        return {'item': item_schema.dump(item)}, 201

    @jwt_required()
    def delete(self, id):
        item = ItemModel.query.filter_by(id = id).first()

        db.session.delete(item)
        db.session.commit()

        return {'message': 'item deleted'}, 200
