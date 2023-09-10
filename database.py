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
    def delete(cls, email):
        cls.col.delete_one({'email': email})

    @classmethod
    def update(cls, email, new_pwd_hash = '', new_email = ''):
        if new_email == '':
            new_email = email
        cls.col.update_one({'email': email}, {"$set": {'email': new_email, 'pwd_hash': new_pwd_hash}})

    @classmethod
    def ping(cls):
        try:
            cls.myclient.admin.command('ping')
            print("Connected to database :D")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    Database.ping()