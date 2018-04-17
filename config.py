from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config['DEBUG'] = os.environ['DEBUG']
app.config['MONGO_DBNAME'] = os.environ['MONGO_DBNAME']
app.config['MONGO_URI'] = os.environ['MONGO_URI']
app.secret_key = os.environ['SECRET_KEY']
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
