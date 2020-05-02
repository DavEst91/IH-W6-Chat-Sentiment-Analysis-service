from pymongo import MongoClient
from bson.json_util import dumps
import pymongo
import pandas as pd
import requests
import nltk
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download("vader_lexicon")
mongodbURL = "mongodb://localhost/Chat_Sentiment_Analysis_Service"
client = MongoClient(mongodbURL, connectTimeoutMS=2000,serverSelectionTimeoutMS=2000)
db = client.get_database()


def value_user(user):
    messages_id=db["users"].find_one({"username":user},{"messages":1})
    messages=[db.messages.find_one({"_id":ident},{"message":1})["message"] for ident in messages_id["messages"]]
    sia = SentimentIntensityAnalyzer()
    valorations=pd.DataFrame(columns=["neg","neu","pos","compound"])
    for sentence in messages:
        scores=sia.polarity_scores(sentence)
        scores_df=pd.DataFrame(data=[scores.values()],columns=["neg","neu","pos","compound"])
        valorations=pd.concat([valorations,scores_df])
    return(valorations.mean().to_json())