from flask_restful import Resource, reqparse

from db import db
from utils.bcrypt import bcrypt

from models.userModel import UserModel

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True)
user_parser.add_argument('password', type=str, required=True)

class UsersRegister(Resource):
    def post(self):
        data = user_parser.parse_args()
        data['password'] = bcrypt.generate_password_hash(data['password'], 10)
        user = UserModel(**data)

        db.session.add(user)
        db.session.commit()

        return {'message': f'User created succesfuly'}, 201