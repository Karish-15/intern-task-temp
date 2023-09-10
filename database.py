import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    url = "mongodb+srv://Karish:" + os.getenv("DB_PASSWORD") + "@cluster0.a7f5vpi.mongodb.net/?retryWrites=true&w=majority"
    myclient = pymongo.MongoClient(url)
    db = myclient['main']
    col = db['Users']

    @classmethod
    def insert(cls, document):
        cls.col.insert_one(document)

    @classmethod
    def delete_by_id(cls, id):
        cls.col.delete_one({'id': id})

    @classmethod
    def update(cls, id = None, pwd_hash = '', email = '', name=''):
        cls.col.update_one({"id": id}, {"$set": {'email': email, 'pwd_hash': pwd_hash, 'name': name, 'id': id}})

    @classmethod
    def ping(cls):
        try:
            cls.myclient.admin.command('ping')
            print("Connected to database :D")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    Database.ping()