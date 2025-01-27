from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from src.controllers.load_database import db
from bson.json_util import dumps
from flask import request
from src.helpers.errorHandler import errorHandler, Error404,APIError
import json
import pymongo
import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
nltk.download("vader_lexicon")


db.conversations.create_index([("conversation_name", pymongo.ASCENDING)], unique=True)

@app.route("/chat/create", methods=["GET","POST"])
@errorHandler
def create_conversation():
    try:
        conversation_name=request.args.get("conversation")
    except:
        raise APIError("Wrong parameters. Try /user/create?conversation=<conversation_name>")
    try:
        db["conversations"].insert_one(
            {"conversation_name":conversation_name,"users":[],"messages":[]}
            )   
        return  {conversation_name:"created!"}
    except:
        raise APIError("This conversation already exists in database")




@app.route("/chat/<conversation_name>/adduser", methods=["GET","POST"])
@errorHandler
def add_user_to_conversation(conversation_name):
    conversation= db['conversations'].find_one({"conversation_name":conversation_name},{"_id":1, "conversation_name":1,"messages":1})        
    if not conversation:
        raise Error404("Conversation doesn't exist in database")
    username=request.args.get("username").lower()
    user = db['users'].find_one({"username":username},{"_id":1,"username":1})
    if user==None:
        raise Error404("User not found in database")
    db["conversations"].update({"_id":conversation["_id"]},{"$addToSet":{"users":username}})
    db["users"].update({"_id":user["_id"]},{"$addToSet":{"conversations":[conversation["conversation_name"],conversation["_id"]]}})
    return {username:f"added to {conversation}"}


@app.route("/chat/<conversation_name>/list", methods=["GET"])
@errorHandler
def list_messages_of_chat(conversation_name):
    conversation= db['conversations'].find_one({"conversation_name":conversation_name},{"_id":1, "conversation_name":1,"users":1,"messages":1})        
    if not conversation:
        raise Error404("Conversation doesn't exist in database")
    pointers=db["messages"].find({"_id":{"$in" :conversation["messages"]}})
    if not pointers:
        raise APIError("Conversation is empty")
    list_of_messages=([{sentence['user'][0]:sentence['message']} for sentence in pointers])
    return(json.dumps(list_of_messages))
   




@app.route("/chat/<conversation_name>/sentiment", methods=["GET"])
@errorHandler
def value_conversation(conversation_name):
    conversation= db['conversations'].find_one({"conversation_name":conversation_name},{"_id":1, "conversation_name":1,"messages":1})        
    if not conversation:
        raise Error404("Conversation doesn't exist in database")
    sia = SentimentIntensityAnalyzer()
    valorations=pd.DataFrame(columns=["neg","neu","pos","compound"])
    sentences=json.loads(list_messages_of_chat(conversation_name))
    for sentence in sentences:
        scores=sia.polarity_scores(list(sentence.values())[0])
        scores_df=pd.DataFrame(data=[scores.values()],columns=["neg","neu","pos","compound"])
        valorations=pd.concat([valorations,scores_df])
    return(valorations.mean().to_json())