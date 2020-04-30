from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from src.controllers.load_database import db
from bson.json_util import dumps
from flask import request
import pymongo

db.users.create_index([("username", pymongo.ASCENDING)], unique=True)

@app.route("/user/<username>")
def get_user_info(username):
    user = db['users'].find({"username":username},{"_id":0, "username":1, "email":1})
    return dumps(user)

@app.route("/user/create", methods=["GET","POST"])
def add_user():
    username=request.args.get("username")
    useremail=request.args.get("useremail")
    print(useremail,1)
    username=username.lower()
    db["users"].insert_one(
        {"username":username,
        "email":useremail  
        }
    )
    return f"User: {username} added to users list!"