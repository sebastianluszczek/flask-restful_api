from flask_restful import Resource, reqparse

from db import db

from models.storeModel import StoreModel, StoreSchema

from flask_jwt import jwt_required

store_parser = reqparse.RequestParser()
store_parser.add_argument('name', type=str, required=True)

stores_schema = StoreSchema(many=True)
store_schema = StoreSchema()

class Stores(Resource):
    @jwt_required()
    def get(self):
        stores = StoreModel.query.all()

        return {'stores': stores_schema.dump(stores)}, 200

    @jwt_required()
    def post(self):
        data = store_parser.parse_args()
        store = StoreModel(**data)

        db.session.add(store)
        db.session.commit()

        return {'store': store_schema.dump(store)}, 201