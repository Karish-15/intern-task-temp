from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

from database import Database

class User(UserMixin):
    """The User model"""

    def __init__(self, _id=None, id=None, name=None, email=None, pwd_hash=None) -> None:
        self.id = int(id)
        self.name = name
        self.email = email
        self.pwd_hash = pwd_hash
        self.generate_document()

    def generate_document(self):
        self.document = {
            'id': self.id,
            'name' : self.name, 
            'email': self.email, 
            'pwd_hash': self.pwd_hash, 
        }

    @staticmethod
    def validate_password(email, password_string):
        try:
            result = Database.col.find_one({'email': email})
        except:
            pass
        else:
            return check_password_hash(result['pwd_hash'], password_string)

    @classmethod
    def get_by_email(cls, email):
        data = Database.col.find_one({'email': email})
        if data is not None:
            return User(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.col.find_one({'id': _id})
        if data is not None:
            return User(**data)

    def save_to_mongo(self, document=None):
        checkUser = User.get_by_id(self.id)
        if(checkUser):
            return [False, "User already exists"]
        if document:
            Database.insert(document)
        else:
            Database.insert(self.document)

        return[True, "User created successfully"]

        return [True, "User created successfully"]

    def update_user(self):
        Database.update(id = self.id, pwd_hash = self.pwd_hash, email = self.email, name = self.name)
        return [True, "User updated successfully"]

    def update_document(self, document):
        self.document = document