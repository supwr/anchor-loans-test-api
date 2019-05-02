from main.database import mongo
from passlib.hash import pbkdf2_sha256 as sha256


class UsersService:

    @staticmethod
    def get_user_by_email_and_username(username, email, fields=None):
        return mongo.db.users.find_one({"$or": [{'username': username}, {'email': email}]}, fields)

    @staticmethod
    def get_user_by_username(username, fields=None):
        return mongo.db.users.find_one({'username': username}, fields)

    @staticmethod
    def new_user(user):
        return mongo.db.users.insert(user)

    @staticmethod
    def get_user_by_id(user_id, fields=None):
        return mongo.db.users.find_one({"_id": user_id}, fields)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
