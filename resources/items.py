from flask_restful import Resource, reqparse

from models.itemModel import ItemModel, ItemSchema

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

    def post(self):
        data = item_parser.parse_args()
        item = ItemModel(**data)

        db.session.add(item)
        db.session.commit()

        return {'item': item_schema.dump(item)}, 201

class Item(Resource):
    def get(self, _id):
        item = ItemModel.query.filter_by(_id = _id).first_or_404(f'No item with _id: {_id}')

        return {'item': item_schema.dump(item)}, 200

    def put(self, _id):
        item = ItemModel.query.filter_by(_id = _id).first_or_404(f'No item with _id: {_id}')

        data = item_parser.parse_args()
        for key, val in data.items():
            setattr(item, key, val)

        db.session.commit()
        
        return {'item': item_schema.dump(item)}, 201

    def delete(self, _id):
        item = ItemModel.query.filter_by(_id = _id).first()

        db.session.delete(item)
        db.session.commit()

        return {'message': 'item deleted'}, 200
