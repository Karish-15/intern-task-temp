from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

from flask_restful import Api
from mongo_api_blueprint.routes import initialize_routes

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['CORS_HEADERS'] = 'Content-Type' 
app.config['SESSION_COOKIE_DOMAIN'] = False
app.config['Access-Control-Allow-Credentials'] = True
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

app = Flask(__name__)

api = Api(app)

initialize_routes(api)

if(__name__ == '__main__'):
    app.run(debug=True)
