import pymongo
import pandas as pd
import requests
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from src.app import app
from pymongo import MongoClient
from src.config import DBURL
from src.controllers.load_database import db
from bson.json_util import dumps
from flask import request
from src.helpers.errorHandler import errorHandler, Error404,APIError
from numpy import abs

nltk.download("vader_lexicon")

#This is the function to calculate score of a single user
def value_user(user):
    messages_id=db["users"].find_one({"username":user},{"messages":1})
    messages_pointer=db.messages.find({"_id":{ "$in": messages_id["messages"]}},{"message":1})
    messages=[sentence["message"] for sentence in messages_pointer]
    sia = SentimentIntensityAnalyzer()
    valorations=pd.DataFrame(columns=["neg","neu","pos","compound"])
    for sentence in list(messages):
        scores=sia.polarity_scores(sentence)
        scores_df=pd.DataFrame(data=[scores.values()],columns=["neg","neu","pos","compound"])
        valorations=pd.concat([valorations,scores_df])
    return(valorations.mean())


#This function should be called when we want to update the puntuations 
#table, for evaluating new users or updating scores of older users
#WARNING: It may take as long as 15 minutes.
def create_df_with_puntuations():
    users=[user["username"] for user in list(db.users.find({},{"username":1}))]
    valorations=pd.DataFrame(columns=["neg","neu","pos","compound"])
    for user in users:
        valoration=pd.DataFrame(data=[value_user(user)],index=[user])
        valorations=pd.concat([valorations,valoration])
    valorations.to_csv("valorations.csv")
    return (valorations)

@app.route("/user/<user_id>/recommend")
@errorHandler
def find_closest_users(user_id):
    user = db['users'].find_one({"username":user_id},{"username":1})
    if not user:
        raise Error404("User not found in database")
    user_puntuation=value_user(user_id).compound
    print(user_puntuation)
    puntuations=pd.read_csv("././output/valorations.csv")
    puntuations["relations"]=abs(puntuations["compound"]-user_puntuation)
    names_index=puntuations.relations.sort_values()[1:4].index
    usernames=[puntuations["Unnamed: 0"][index] for index in names_index]
    return {"closest_users":" , ".join(usernames)}