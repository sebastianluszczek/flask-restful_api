from flask import Flask, request
from flask_restful import Resource, Api, reqparse

from uuid import uuid4

app = Flask(__name__)
api = Api(app)

items = []

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('price', type=float, required=True)


class Items(Resource):
    def get(self):
        return {'items': items}, 200

    def post(self):
        data = parser.parse_args()
        data['id'] = str(uuid4())
        items.append(data)
        return {'item': data}, 201

class Item(Resource):
    def get(self, id):
        item = next(filter(lambda x: x['id'] == id, items), None)
        return {'item': item}, 200 if item else 404
    
    def put(self, id):
        data = parser.parse_args()
        item = next(filter(lambda x: x['id'] == id, items), None)

        if item:
            item.update(data)
            return {'item': item}, 200
        else:
            data['id'] = id
            items.append(data)
            return {'item': data}, 201

    def delete(self, id):
        global items
        items = list(filter(lambda x: x['id'] != id, items))
        return {'message': f'item {id} deleted'}, 200
        

api.add_resource(Items, '/items')
api.add_resource(Item, '/items/<string:id>')

