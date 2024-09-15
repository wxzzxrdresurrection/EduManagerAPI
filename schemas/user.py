from bson import ObjectId
from config.db import MongoConnection
from models.user_model import authenticate_user, create_access_token
class UserSchema:
    def __init__(self):
        self.mongo = MongoConnection()
        self.users = []

    def get_users(self):
        users = self.mongo.get_collection("users")
        if not users:
            return []
        for user in users:
            user['id'] = str(user.pop('_id'))
            self.users.append(user)
        return self.users

    def get_user(self, user_id):
        user = self.mongo.get_item_from_collection_by_id("users", ObjectId(user_id))
        return user

    def add_user(self, user):
        data = self.mongo.insert_item_into_collection("users", user.dict())
        return data
    
    def login(self, user):
        user, message = authenticate_user(self.mongo, user.email, user.password)
        if user:     
            token = create_access_token(user)
        else:
            token = ""
        return user, message, token