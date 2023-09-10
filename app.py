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

@app.route('/users', method=['GET'])
def get_users():
    all_users = Database.col.find()
    status = 200
    if(all_users):
        return jsonify(all_users), status

    return jsonify({"message": "No users found"}), 400

@app.route('/users/<id>', method=['GET'])
def get_user_by_id(id):
    user = User.get_by_id(id)
    if(user):
        return jsonify(user), 200

    return jsonify({"message": "No user found from given ID"}), 400

