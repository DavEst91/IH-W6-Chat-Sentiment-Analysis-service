from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from src.controllers.load_database import db
from bson.json_util import dumps
from flask import request
from src.helpers.errorHandler import errorHandler, Error404,APIError

import pymongo

db.users.create_index([("username", pymongo.ASCENDING)], unique=True)

@app.route("/user/<username>")
@errorHandler
def get_user_info(username):
    user = db['users'].find_one({"username":username},{"_id":1, "username":1,"conversations":1,"messages":1})
    if user==None:
        raise Error404("User not found in database")
    return dumps(user)



@app.route("/user/create", methods=["GET","POST"])
@errorHandler
def add_user():
    try:
        username=request.args.get("username").lower()
    except:
        raise APIError("Wrong parameters. Try /user/create?username=<username>")
    #This step is neccesary because mongo method insert_one does not manage correctly uniquenness of the username
    user = db['users'].find_one({"username":username},{"_id":1, "username":1,"conversations":1,"messages":1})
    if user!=None:
        raise APIError("This user already exists in database")
    try:
        db["users"].insert_one(
            {"username":username,
             "conversations":[],
             "messages":[]
            }
            )   
        return  {username:"added to users list!"}
    except:
        raise APIError("This user already exists in database")
