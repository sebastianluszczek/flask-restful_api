from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.itemResources import Item, Items
from resources.storeResources import Stores
from resources.authResources import UsersRegister

from utils.auth import authenticate, identity
from utils.db import db, ma
from utils.bcrypt import bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sebastian:pass123@localhost/flask_restful_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_AUTH_URL_RULE'] = '/auth/login'

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)

api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Items, '/items', endpoint='items')
api.add_resource(Item, '/items/<id>', endpoint='item')

api.add_resource(Stores, '/stores', endpoint='stores')

api.add_resource(UsersRegister, '/auth/register', endpoint='register')