from pymongo import MongoClient
from dotenv import load_dotenv
import os

class MongoConnection:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://devluiszapata:99zvOAejXk6cPnyc@edumanager.ac5ko.mongodb.net/?retryWrites=true&w=majority&appName=EduManager")
        self.db = self.client.EduManager
        self.test_connection()

    def test_connection(self):
        try:
            self.client.server_info()
            print("Connection successful")
        except Exception as e:
            print(e)
            return False
        
    def get_collection(self, collection_name):
        collection = self.db[collection_name]
        data = collection.find()
        print(data)
        print(collection)
        return "collection"
    