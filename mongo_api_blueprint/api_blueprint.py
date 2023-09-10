from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse
from werkzeug.security import generate_password_hash

from models import User
from database import Database

api_bp = Blueprint('api_blueprint', __name__)

class User_details(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("id", required=True, location="form")
    parser.add_argument("name", required=True, location="form")
    parser.add_argument("name", required=True, location="form")
    parser.add_argument("password", required=True, location="form")

    def get(self):
        all_users = Database.col.find()
        users_list = []

        if(all_users):
            for user in all_users:
                user_data = {}
                user_data = {'Id': user['id'], 'Name': user['name'], 'Email': user['email']}
                users_list.append(user_data)

            response = {'Number of users': len(users_list), 'Users': users_list}
            return response, 200

        return ({"message": "No users found"}), 400

    def post(self):
        args = self.parser.parse_args()
        request_data = args

        if(request_data):
            data = request_data
            password = data['password']
            data['pwd_hash'] = generate_password_hash(password)
            del data['password']

            user = User(**data)
            response = user.save_to_mongo()
            if(response[0]):
                return ({"message": response[1]}), 200
            
            return ({"message": response[1]}), 400
        
        return ({"message": "No data received"}), 400


class User_by_id(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("id", required=True, location="form")
    parser.add_argument("name", required=True, location="form")
    parser.add_argument("email", required=True, location="form")
    parser.add_argument("password", required=True, location="form")

    def get(self, id):
        user = User.get_by_id(int(id))
        if(user):
            user_data = {}
            user_data = {'Id': user.id, 'Name': user.name, 'Email': user.email}
            return (user_data), 200

        return ({"message": "No user found from given ID"}), 400

    def put(self, id):
        args = self.parser.parse_args()
        request_data = args

        if(request_data):
            data = request_data
            password = data['password']
            data['pwd_hash'] = generate_password_hash(password)
            del data['password']

            user_to_update  = User.get_by_id(int(request_data['id']))

            if(user_to_update is None):
                return ({"message": "No user found from given ID"}), 400

            # Assign new values to user object
            user_to_update.name = request_data['name']
            user_to_update.email = request_data['email']
            user_to_update.pwd_hash = request_data['pwd_hash']
            user_to_update.generate_document()
            
            # Update user in database
            response = user_to_update.update_user()
            
            if(response[0]):
                return (response[1]), 200
            
            return (response[1]), 400
    
        return ({"message": "No data received"}), 400

    def delete(self, id):
        user = User.get_by_id(int(id))
        if(user):
            Database.delete_by_id(user.id)
            return ({"message": "User deleted successfully"}), 200

        return ({"message": "No user found from given ID"}), 400