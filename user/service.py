from config import mongo, bcrypt
from .model import User
import pymongo
from exception import AbortException, NotFoundException
import re


def create_user(name, email, role, password):
    user = mongo.db.users
    user.create_index([('email', pymongo.TEXT)], unique=True)
    pw_hash = bcrypt.generate_password_hash(password)
    pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if not pattern.match(email):
        raise AbortException("email not valid")
    try:
        user_id = user.insert({'name': name, 'email': email, 'role': role, 'password': pw_hash})
    except Exception as e:
        raise AbortException("email {} already exist".format(email))
    new_user = user.find_one({'_id': user_id})
    new_user = User(name=new_user['name'], role=new_user['role'], email=new_user['email'])
    return new_user


def get_user(email):
    user = mongo.db.users
    user = user.find_one({'email': email})
    if not user:
        raise NotFoundException("user with email {} not found".format(email))
    user = User(name=user['name'], role=user['role'], email=user['email'])
    return user


def authenticate(email, password):
    user = mongo.db.users
    print(email)
    user = user.find_one({'email': email})
    print(user)
    if not user:
        raise NotFoundException("user with email {} not found".format(email))
    if bcrypt.check_password_hash(user['password'], password):
        user = User(name=user['name'], role=user['role'], email=user['email'])
        return user
    raise AbortException("password not match")
