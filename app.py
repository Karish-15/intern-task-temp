from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

from models import User
from database import Database

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['CORS_HEADERS'] = 'Content-Type' 
app.config['SESSION_COOKIE_DOMAIN'] = False
app.config['Access-Control-Allow-Credentials'] = True
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

@app.route('/users', methods=['GET'])
def get_users():
    all_users = Database.col.find()
    users_list = []

    if(all_users):
        for user in all_users:
            user_data = {}
            user_data = {'Id': user['id'], 'Name': user['name'], 'Email': user['email']}
            users_list.append(user_data)

        response = {'Number of users': len(users_list), 'Users': users_list}

        return jsonify(response), 200

    return jsonify({"message": "No users found"}), 400

@app.route('/users/<id>', methods=['GET'])
def get_user_by_id(id):
    user = User.get_by_id(int(id))
    if(user):
        user_data = {}
        user_data = {'Id': user.id, 'Name': user.name, 'Email': user.email}
        return jsonify(user_data), 200

    return jsonify({"message": "No user found from given ID"}), 400

@app.route('/users', methods=['POST'])
def create_user():
    request_data = request.form.to_dict()

    if(request_data):
        data = request_data
        password = data['password']
        data['pwd_hash'] = generate_password_hash(password)
        del data['password']

        user = User(**data)
        response = user.save_to_mongo()
        if(response[0]):
            return jsonify({"message": response[1]}), 200
        
        return jsonify({"message": response[1]}), 400
    
    return jsonify({"message": "No data received"}), 400

@app.route('/users/<id>', methods=['PUT'])
def update_user_data(id):
    request_data = request.form.to_dict()

    if(request_data):
        data = request_data
        password = data['password']
        data['pwd_hash'] = generate_password_hash(password)
        del data['password']

        user_to_update  = User.get_by_id(int(request_data['id']))

        if(user_to_update is None):
            return jsonify({"message": "No user found from given ID"}), 400

        # Assign new values to user object
        user_to_update.name = request_data['name']
        user_to_update.email = request_data['email']
        user_to_update.pwd_hash = request_data['pwd_hash']
        user_to_update.generate_document()
        
        # Update user in database
        response = user_to_update.update_user()
        
        if(response[0]):
            return jsonify(response[1]), 200
        
        return jsonify(response[1]), 400
    
    return jsonify({"message": "No data received"}), 400

@app.route('/users/<id>', methods=['DELETE'])
def delete_user_by_id(id):
    user = User.get_by_id(int(id))
    if(user):
        Database.delete_by_id(user.id)
        return jsonify({"message": "User deleted successfully"}), 200

    return jsonify({"message": "No user found from given ID"}), 400


if __name__ == '__main__':
    # Database.ping()
    app.run(debug=True)
