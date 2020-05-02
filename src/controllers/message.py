from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from src.controllers.load_database import db
from bson.json_util import dumps
from flask import request
from src.helpers.errorHandler import errorHandler, Error404,APIError

import pymongo


@app.route("/chat/<conversation_name>/addmessage")
#@errorHandler
def add_message(conversation_name):

    conversation= db['conversations'].find_one({"conversation_name":conversation_name},{"_id":1, "conversation_name":1,"users":1})        
    if not conversation:
        raise Error404("Conversation doesn't exist in database")
    username=request.args.get("username").lower()
    user = db['users'].find_one({"username":username},{"username":1})
    if not user:
        raise Error404("User not found in database")
    if user["username"] not in conversation["users"]:
        raise APIError("User is not in this conversation.Please, add it first")

    message=request.args.get("message").replace("%20"," ")
    message_id=db["messages"].insert_one(
            {"message":message,
             "user":[username,user["_id"]],
             "conversation":[conversation["conversation_name"],conversation["_id"]]}).inserted_id
    db["users"].update({"_id":user["_id"]},{"$addToSet":{"messages":message_id}})
    db["conversations"].update({"_id":conversation["_id"]},{"$addToSet":{"messages":message_id}})
    print("hola")
    return (f"{{'message_id':{message_id}}}")





