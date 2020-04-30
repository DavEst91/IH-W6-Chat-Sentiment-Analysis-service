from src.app import app
from pymongo import MongoClient
from src.config import DBURL

client = MongoClient(DBURL)
print(f"Connected to {DBURL}")
db = client.get_database()


