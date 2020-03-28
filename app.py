from flask import Flask
from flask_restful import Api

from resources.itemResources import Item, Items
from resources.storeResources import Stores

from db import db, ma

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sebastian:pass123@localhost/flask_restful_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(ma)

api = Api(app)

api.add_resource(Items, '/items', endpoint='items')
api.add_resource(Item, '/items/<id>', endpoint='item')

api.add_resource(Stores, '/stores', endpoint='stores')