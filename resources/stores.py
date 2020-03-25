from flask_restful import Resource, reqparse

from models.storeModel import StoreModel, StoreSchema

store_parser = reqparse.RequestParser()
store_parser.add_argument('name', type=str, required=True)

stores_schema = StoreSchema(many=True)
store_schema = StoreSchema()

class Stores(Resource):
    def get(self):
        stores = StoreModel.query.all()

        return {'stores': stores_schema.dump(stores)}, 200

    def post(self):
        data = store_parser.parse_args()
        store = StoreModel(**data)

        db.session.add(store)
        db.session.commit()

        return {'item': store_schema.dump(store)}, 201