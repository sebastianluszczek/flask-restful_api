from flask import Flask, request        
from flask_restful import Resource, Api

from uuid import uuid4

app = Flask(__name__)
api = Api(app)

items = []

class Items(Resource):
    def get(self):
        return {'items': items}, 200

    def post(self):                     
        data = request.get_json()
        data['_id'] = str(uuid4())      
        items.append(data)              
        return {'item': data}, 201  

class Item(Resource):                           #new
    def get(self, _id):                         #new
        pass                                    #new    

    def put(self, _id):                         #new
        pass                                    #new

    def delete(self, _id):                      #new
        pass                                    #new

api.add_resource(Items, '/items')
api.add_resource(Item, '/items/<string:_id>')   #new

if __name__ == '__main__':
    app.run(debug=True)